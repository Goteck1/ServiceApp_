import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.professional import Professional
from src.models.service_request import ServiceRequest
from src.models.review import Review
from src.routes.user import user_bp
from src.routes.professional import professional_bp
from src.routes.service_request import service_request_bp
from src.routes.review import review_bp
from src.routes.auth import auth_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(professional_bp, url_prefix='/api')
app.register_blueprint(service_request_bp, url_prefix='/api')
app.register_blueprint(review_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_sample_data():
    """Initialize sample data for testing"""
    import json
    
    # Check if data already exists
    if Professional.query.first():
        return
    
    # Sample professionals
    professionals_data = [
        {
            'name': 'Juan Pérez',
            'category': 'electricista',
            'rating': 4.8,
            'reviews_count': 127,
            'distance': '0.5 km',
            'available': True,
            'specialties': ['Instalaciones', 'Reparaciones'],
            'price': '$5,000',
            'avatar': 'JP',
            'phone': '+54 9 342 123-4567',
            'description': 'Electricista con más de 10 años de experiencia en instalaciones residenciales y comerciales.'
        },
        {
            'name': 'María González',
            'category': 'electricista',
            'rating': 4.9,
            'reviews_count': 89,
            'distance': '1.2 km',
            'available': True,
            'specialties': ['Instalaciones', 'Mantenimiento'],
            'price': '$4,500',
            'avatar': 'MG',
            'phone': '+54 9 342 234-5678',
            'description': 'Especialista en sistemas eléctricos modernos y domótica.'
        },
        {
            'name': 'Carlos Rodríguez',
            'category': 'electricista',
            'rating': 4.7,
            'reviews_count': 156,
            'distance': '2.1 km',
            'available': False,
            'specialties': ['Reparaciones', 'Emergencias'],
            'price': '$6,000',
            'avatar': 'CR',
            'phone': '+54 9 342 345-6789',
            'description': 'Servicio de emergencias 24/7 para reparaciones eléctricas urgentes.'
        },
        {
            'name': 'Ana Martínez',
            'category': 'plomero',
            'rating': 4.9,
            'reviews_count': 203,
            'distance': '0.8 km',
            'available': True,
            'specialties': ['Reparaciones', 'Instalaciones'],
            'price': '$4,000',
            'avatar': 'AM',
            'phone': '+54 9 342 456-7890',
            'description': 'Plomera especializada en reparaciones de cañerías y grifería.'
        },
        {
            'name': 'Luis Fernández',
            'category': 'carpintero',
            'rating': 4.8,
            'reviews_count': 98,
            'distance': '1.5 km',
            'available': True,
            'specialties': ['Muebles', 'Reparaciones'],
            'price': '$3,500',
            'avatar': 'LF',
            'phone': '+54 9 342 567-8901',
            'description': 'Carpintero artesanal especializado en muebles a medida y restauración.'
        }
    ]
    
    for prof_data in professionals_data:
        professional = Professional(
            name=prof_data['name'],
            category=prof_data['category'],
            rating=prof_data['rating'],
            reviews_count=prof_data['reviews_count'],
            distance=prof_data['distance'],
            available=prof_data['available'],
            specialties=json.dumps(prof_data['specialties']),
            price=prof_data['price'],
            avatar=prof_data['avatar'],
            phone=prof_data['phone'],
            description=prof_data['description']
        )
        db.session.add(professional)
    
    # Sample reviews
    reviews_data = [
        {
            'professional_id': 1,
            'client_name': 'Ana Cliente',
            'client_avatar': 'AC',
            'rating': 5,
            'comment': 'Excelente trabajo, muy profesional y puntual.'
        },
        {
            'professional_id': 1,
            'client_name': 'José Morales',
            'client_avatar': 'JM',
            'rating': 4,
            'comment': 'Buen servicio, resolvió el problema rápidamente.'
        },
        {
            'professional_id': 2,
            'client_name': 'Laura Pérez',
            'client_avatar': 'LP',
            'rating': 5,
            'comment': 'Muy recomendable, trabajo de calidad.'
        },
        {
            'professional_id': 4,
            'client_name': 'Roberto Silva',
            'client_avatar': 'RS',
            'rating': 5,
            'comment': 'Solucionó la fuga de agua perfectamente.'
        }
    ]
    
    for review_data in reviews_data:
        review = Review(
            professional_id=review_data['professional_id'],
            client_name=review_data['client_name'],
            client_avatar=review_data['client_avatar'],
            rating=review_data['rating'],
            comment=review_data['comment']
        )
        db.session.add(review)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    init_sample_data()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
