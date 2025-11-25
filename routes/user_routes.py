from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('', methods=['POST'])
def create_user():
    """Endpoint for create user"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data sent'}), 400
    
    name = data.get('name')
    email = data.get('email')
    
    result = UserController.create_user(name, email)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@user_bp.route('', methods=['GET'])
def get_all_users():
    """Endpoint for listing all users"""
    result = UserController.get_all_users()
    
    if result['success']:
        return jsonify({
            'users': result['data'],
            'total': result['count']
        }), 200
    else:
        return jsonify(result), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint to get a specific user"""
    result = UserController.get_user(user_id)
    
    if result['success']:
        return jsonify(result['data']), 200
    else:
        return jsonify(result), 404

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Endpoint to delete a user"""
    result = UserController.delete_user(user_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404