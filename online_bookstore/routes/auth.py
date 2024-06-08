from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import User, db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify(access_token=access_token)

@auth_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(username=user_identity['username']).first()
    if user.role != 'admin':
        return jsonify({'message': 'Admins only!'}), 403
    return jsonify({'message': 'Welcome, admin!'})
