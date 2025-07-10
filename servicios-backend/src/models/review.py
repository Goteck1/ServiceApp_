from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_avatar = db.Column(db.String(10), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    professional = db.relationship('Professional', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f'<Review {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'professional_id': self.professional_id,
            'client_name': self.client_name,
            'client_avatar': self.client_avatar,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

