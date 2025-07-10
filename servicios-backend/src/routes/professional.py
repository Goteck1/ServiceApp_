from flask import Blueprint, jsonify, request
from src.models.professional import Professional, db
from src.models.review import Review

professional_bp = Blueprint('professional', __name__)

@professional_bp.route('/professionals', methods=['GET'])
def get_professionals():
    """Obtener todos los profesionales o filtrar por categoría"""
    category = request.args.get('category')
    
    if category:
        professionals = Professional.query.filter_by(category=category).all()
    else:
        professionals = Professional.query.all()
    
    return jsonify([professional.to_dict() for professional in professionals])

@professional_bp.route('/professionals/<int:professional_id>', methods=['GET'])
def get_professional(professional_id):
    """Obtener un profesional específico"""
    professional = Professional.query.get_or_404(professional_id)
    return jsonify(professional.to_dict())

@professional_bp.route('/professionals', methods=['POST'])
def create_professional():
    """Crear un nuevo profesional"""
    data = request.json
    import json
    
    professional = Professional(
        name=data['name'],
        category=data['category'],
        rating=data.get('rating', 0.0),
        reviews_count=data.get('reviews_count', 0),
        distance=data['distance'],
        available=data.get('available', True),
        specialties=json.dumps(data.get('specialties', [])),
        price=data['price'],
        avatar=data['avatar'],
        phone=data.get('phone'),
        description=data.get('description'),
        location=data.get('location', 'Santa Fe')
    )
    
    db.session.add(professional)
    db.session.commit()
    return jsonify(professional.to_dict()), 201

@professional_bp.route('/professionals/<int:professional_id>', methods=['PUT'])
def update_professional(professional_id):
    """Actualizar un profesional"""
    professional = Professional.query.get_or_404(professional_id)
    data = request.json
    import json
    
    professional.name = data.get('name', professional.name)
    professional.category = data.get('category', professional.category)
    professional.rating = data.get('rating', professional.rating)
    professional.reviews_count = data.get('reviews_count', professional.reviews_count)
    professional.distance = data.get('distance', professional.distance)
    professional.available = data.get('available', professional.available)
    if 'specialties' in data:
        professional.specialties = json.dumps(data['specialties'])
    professional.price = data.get('price', professional.price)
    professional.avatar = data.get('avatar', professional.avatar)
    professional.phone = data.get('phone', professional.phone)
    professional.description = data.get('description', professional.description)
    professional.location = data.get('location', professional.location)
    
    db.session.commit()
    return jsonify(professional.to_dict())

@professional_bp.route('/professionals/<int:professional_id>', methods=['DELETE'])
def delete_professional(professional_id):
    """Eliminar un profesional"""
    professional = Professional.query.get_or_404(professional_id)
    db.session.delete(professional)
    db.session.commit()
    return '', 204

@professional_bp.route('/professionals/<int:professional_id>/reviews', methods=['GET'])
def get_professional_reviews(professional_id):
    """Obtener las reseñas de un profesional"""
    professional = Professional.query.get_or_404(professional_id)
    reviews = Review.query.filter_by(professional_id=professional_id).order_by(Review.created_at.desc()).all()
    return jsonify([review.to_dict() for review in reviews])

@professional_bp.route('/categories', methods=['GET'])
def get_categories():
    """Obtener todas las categorías disponibles"""
    categories = [
        {'id': 'electricista', 'name': 'Electricista', 'icon': 'zap'},
        {'id': 'plomero', 'name': 'Plomero', 'icon': 'droplets'},
        {'id': 'carpintero', 'name': 'Carpintero', 'icon': 'hammer'},
        {'id': 'pintor', 'name': 'Pintor', 'icon': 'paintbrush'},
        {'id': 'mecanico', 'name': 'Mecánico', 'icon': 'wrench'},
        {'id': 'peluquero', 'name': 'Peluquero', 'icon': 'scissors'}
    ]
    return jsonify(categories)

