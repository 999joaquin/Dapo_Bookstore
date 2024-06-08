from flask import Blueprint, request, jsonify
from models import Wishlist, Book, db
from flask_jwt_extended import jwt_required, get_jwt_identity

wishlist_bp = Blueprint('wishlist_bp', __name__)

@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_identity = get_jwt_identity()
    wishlist = Wishlist.query.filter_by(user_id=user_identity['id']).all()
    books = [Book.query.get(item.book_id).to_dict() for item in wishlist]
    return jsonify(books)

@wishlist_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    data = request.get_json()
    user_identity = get_jwt_identity()
    new_wishlist_item = Wishlist(user_id=user_identity['id'], book_id=data['book_id'])
    db.session.add(new_wishlist_item)
    db.session.commit()
    return jsonify({'message': 'Book added to wishlist'}), 201

@wishlist_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(book_id):
    user_identity = get_jwt_identity()
    Wishlist.query.filter_by(user_id=user_identity['id'], book_id=book_id).delete()
    db.session.commit()
    return jsonify({'message': 'Book removed from wishlist'}), 204
