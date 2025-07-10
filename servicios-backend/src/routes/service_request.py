from flask import Blueprint, jsonify, request
from src.models.service_request import ServiceRequest, db
from src.models.professional import Professional
from datetime import datetime

service_request_bp = Blueprint('service_request', __name__)

@service_request_bp.route('/service-requests', methods=['GET'])
def get_service_requests():
    """Obtener todas las solicitudes de servicio"""
    professional_id = request.args.get('professional_id')
    
    if professional_id:
        requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()
    else:
        requests = ServiceRequest.query.all()
    
    return jsonify([req.to_dict() for req in requests])

@service_request_bp.route('/service-requests/<int:request_id>', methods=['GET'])
def get_service_request(request_id):
    """Obtener una solicitud específica"""
    service_request = ServiceRequest.query.get_or_404(request_id)
    return jsonify(service_request.to_dict())

@service_request_bp.route('/service-requests', methods=['POST'])
def create_service_request():
    """Crear una nueva solicitud de servicio"""
    data = request.json
    
    # Validar que el profesional existe
    professional = Professional.query.get_or_404(data['professional_id'])
    
    # Parsear fecha y hora
    service_date = datetime.strptime(data['service_date'], '%Y-%m-%d').date()
    service_time = datetime.strptime(data['service_time'], '%H:%M').time()
    
    service_request = ServiceRequest(
        client_name=data['client_name'],
        client_phone=data['client_phone'],
        professional_id=data['professional_id'],
        service_date=service_date,
        service_time=service_time,
        address=data['address'],
        description=data['description'],
        estimated_budget=data.get('estimated_budget'),
        status='pending'
    )
    
    db.session.add(service_request)
    db.session.commit()
    return jsonify(service_request.to_dict()), 201

@service_request_bp.route('/service-requests/<int:request_id>', methods=['PUT'])
def update_service_request(request_id):
    """Actualizar una solicitud de servicio"""
    service_request = ServiceRequest.query.get_or_404(request_id)
    data = request.json
    
    service_request.client_name = data.get('client_name', service_request.client_name)
    service_request.client_phone = data.get('client_phone', service_request.client_phone)
    
    if 'service_date' in data:
        service_request.service_date = datetime.strptime(data['service_date'], '%Y-%m-%d').date()
    
    if 'service_time' in data:
        service_request.service_time = datetime.strptime(data['service_time'], '%H:%M').time()
    
    service_request.address = data.get('address', service_request.address)
    service_request.description = data.get('description', service_request.description)
    service_request.estimated_budget = data.get('estimated_budget', service_request.estimated_budget)
    service_request.status = data.get('status', service_request.status)
    
    db.session.commit()
    return jsonify(service_request.to_dict())

@service_request_bp.route('/service-requests/<int:request_id>', methods=['DELETE'])
def delete_service_request(request_id):
    """Eliminar una solicitud de servicio"""
    service_request = ServiceRequest.query.get_or_404(request_id)
    db.session.delete(service_request)
    db.session.commit()
    return '', 204

@service_request_bp.route('/service-requests/<int:request_id>/status', methods=['PUT'])
def update_request_status(request_id):
    """Actualizar solo el estado de una solicitud"""
    service_request = ServiceRequest.query.get_or_404(request_id)
    data = request.json
    
    valid_statuses = ['pending', 'accepted', 'rejected', 'completed']
    if data.get('status') not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    service_request.status = data['status']
    db.session.commit()
    return jsonify(service_request.to_dict())

