from flask import Flask, request, jsonify, make_response
import requests
import pika
import threading
import json
from database import insert_data

app = Flask(__name__)
book_service = "http://127.0.0.1:5001"
author_service = "http://127.0.0.1:5002"

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received event data:", data)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='book_created')
    channel.basic_consume(queue='book_created', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()

consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()

@app.route("/", methods=["GET"])
def index():
    return "Welcome to Order Service"

@app.route("/order", methods=["POST"])
def create_order():
    data_post = request.get_json()
    data_allowed = ["book_id", "quantity"]
    data_post_empty = [key for key in data_allowed if key not in data_post or data_post[key] == ""]
    
    if data_post_empty:
        return make_response(jsonify({"status": 400, "message": "Some form data is missing", "empty_form": data_post_empty}))
    
    book_id = data_post["book_id"]
    book_response = requests.get(f"{book_service}/book/{book_id}")
    if book_response.status_code != 200:
        return make_response(jsonify({"status": 404, "message": "Book not found"}))
    book_data = book_response.json()
    
    author_response = requests.get(f"{author_service}/author/{book_data['author_id']}")
    if author_response.status_code != 200:
        return make_response(jsonify({"status": 404, "message": "Author not found"}))
    author_data = author_response.json()
    
    total_price = int(data_post["quantity"]) * 100  # Mock price calculation
    order_details = {
        "book": book_data,
        "author": author_data,
        "quantity": data_post["quantity"],
        "total_price": total_price
    }
    
    # Insert the new order into the database
    new_order = {
        "book_id": book_id,
        "quantity": data_post["quantity"],
        "total_price": total_price
    }
    insert_data("orders", new_order)
    
    return make_response(jsonify({"status": 200, "order_details": order_details}))

if __name__ == "__main__":
    app.run(port=5003, debug=True)
