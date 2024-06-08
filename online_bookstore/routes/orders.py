import pika
import json
from flask import Blueprint, request, jsonify
from models import Order, Book, db
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders_bp', __name__)

def publish_stock_update(book_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='stock_updates')

    message = {'book_id': book_id}
    channel.basic_publish(exchange='', routing_key='stock_updates', body=json.dumps(message))
    connection.close()

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_identity = get_jwt_identity()
    book = Book.query.get_or_404(data['book_id'])
    if book.stock < data['quantity']:
        return jsonify({'message': 'Not enough stock'}), 400
    total_price = book.price * data['quantity']
    new_order = Order(
        user_id=user_identity['id'],
        book_id=book.id,
        quantity=data['quantity'],
        total_price=total_price
    )
    book.stock -= data['quantity']
    db.session.add(new_order)
    db.session.commit()

    # Publish stock update event
    publish_stock_update(book.id)

    return jsonify(new_order.to_dict()), 201

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())
