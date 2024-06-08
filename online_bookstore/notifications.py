import pika
import json
from models import Wishlist, User, Book, db

def callback(ch, method, properties, body):
    message = json.loads(body)
    book_id = message['book_id']
    wishlists = Wishlist.query.filter_by(book_id=book_id).all()
    for wishlist in wishlists:
        user = User.query.get(wishlist.user_id)
        book = Book.query.get(book_id)
        # Logic to notify users about the stock update
        print(f"Notify {user.email}: {book.title} is back in stock!")

def consume_stock_updates():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='stock_updates')

    channel.basic_consume(queue='stock_updates', on_message_callback=callback, auto_ack=True)
    print('Waiting for stock updates. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    consume_stock_updates()
