from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    distance = db.Column(db.String(20), nullable=False)
    available = db.Column(db.Boolean, default=True)
    specialties = db.Column(db.Text)  # JSON string of specialties
    price = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    location = db.Column(db.String(100), default='Santa Fe')

    def __repr__(self):
        return f'<Professional {self.name}>'

    def to_dict(self):
        import json
        specialties_list = []
        if self.specialties:
            try:
                specialties_list = json.loads(self.specialties)
            except:
                specialties_list = [self.specialties]
        
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'distance': self.distance,
            'available': self.available,
            'specialties': specialties_list,
            'price': self.price,
            'avatar': self.avatar,
            'phone': self.phone,
            'description': self.description,
            'location': self.location
        }

