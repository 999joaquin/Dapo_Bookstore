from flask import Flask, request, jsonify, make_response, render_template
import json
import pika
from database import insert_data, get_data

app = Flask(__name__, template_folder='templates', static_folder='static')

def publish_message(queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)
    connection.close()

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/books", methods=["GET"])
def get_books():
    books = get_data("SELECT * FROM books")
    if books:
        books_list = [{"id": book[0], "title": book[1], "author_id": book[2]} for book in books]
        return make_response(jsonify({"books": books_list}))
    else:
        return make_response(jsonify({"books": []}))

@app.route("/book/<int:id>", methods=["GET"])
def get_book(id):
    book = get_data(f"SELECT * FROM books WHERE id={id}")
    if book:
        book_data = {"id": book[0][0], "title": book[0][1], "author_id": book[0][2]}
        return make_response(jsonify(book_data))
    else:
        return make_response(jsonify({"message": "Book not found"}), 404)

@app.route("/create_book", methods=["POST"])
def create_book():
    data = request.get_json()
    new_book = {"id": data["id"], "title": data["title"], "author_id": data["author_id"]}
    insert_data("books", new_book)
    publish_message('book_created', json.dumps(new_book))
    return make_response(jsonify({"status": "success", "data": new_book}))

if __name__ == "__main__":
    app.run(port=5001, debug=True)
