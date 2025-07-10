from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    service_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_budget = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    professional = db.relationship('Professional', backref=db.backref('service_requests', lazy=True))

    def __repr__(self):
        return f'<ServiceRequest {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_phone': self.client_phone,
            'professional_id': self.professional_id,
            'professional_name': self.professional.name if self.professional else None,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'service_time': self.service_time.strftime('%H:%M') if self.service_time else None,
            'address': self.address,
            'description': self.description,
            'estimated_budget': self.estimated_budget,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

