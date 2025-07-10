from flask import Blueprint, jsonify, request
from src.models.review import Review, db
from src.models.professional import Professional

review_bp = Blueprint('review', __name__)

@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Obtener todas las reseñas"""
    professional_id = request.args.get('professional_id')
    
    if professional_id:
        reviews = Review.query.filter_by(professional_id=professional_id).order_by(Review.created_at.desc()).all()
    else:
        reviews = Review.query.order_by(Review.created_at.desc()).all()
    
    return jsonify([review.to_dict() for review in reviews])

@review_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Obtener una reseña específica"""
    review = Review.query.get_or_404(review_id)
    return jsonify(review.to_dict())

@review_bp.route('/reviews', methods=['POST'])
def create_review():
    """Crear una nueva reseña"""
    data = request.json
    
    # Validar que el profesional existe
    professional = Professional.query.get_or_404(data['professional_id'])
    
    # Validar rating
    rating = data.get('rating', 0)
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    review = Review(
        professional_id=data['professional_id'],
        client_name=data['client_name'],
        client_avatar=data['client_avatar'],
        rating=rating,
        comment=data['comment']
    )
    
    db.session.add(review)
    
    # Actualizar el rating promedio del profesional
    all_reviews = Review.query.filter_by(professional_id=data['professional_id']).all()
    if all_reviews:
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        professional.rating = round(avg_rating, 1)
        professional.reviews_count = len(all_reviews)
    
    db.session.commit()
    return jsonify(review.to_dict()), 201

@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """Actualizar una reseña"""
    review = Review.query.get_or_404(review_id)
    data = request.json
    
    # Validar rating si se proporciona
    if 'rating' in data:
        rating = data['rating']
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        review.rating = rating
    
    review.client_name = data.get('client_name', review.client_name)
    review.client_avatar = data.get('client_avatar', review.client_avatar)
    review.comment = data.get('comment', review.comment)
    
    # Recalcular el rating promedio del profesional
    professional = Professional.query.get(review.professional_id)
    if professional:
        all_reviews = Review.query.filter_by(professional_id=review.professional_id).all()
        if all_reviews:
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            professional.rating = round(avg_rating, 1)
            professional.reviews_count = len(all_reviews)
    
    db.session.commit()
    return jsonify(review.to_dict())

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Eliminar una reseña"""
    review = Review.query.get_or_404(review_id)
    professional_id = review.professional_id
    
    db.session.delete(review)
    
    # Recalcular el rating promedio del profesional
    professional = Professional.query.get(professional_id)
    if professional:
        remaining_reviews = Review.query.filter_by(professional_id=professional_id).all()
        if remaining_reviews:
            avg_rating = sum(r.rating for r in remaining_reviews) / len(remaining_reviews)
            professional.rating = round(avg_rating, 1)
            professional.reviews_count = len(remaining_reviews)
        else:
            professional.rating = 0.0
            professional.reviews_count = 0
    
    db.session.commit()
    return '', 204

