from models import Book, Order, db
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    if not orders:
        return []

    # Get a list of all book IDs
    all_books = Book.query.all()
    book_ids = [book.id for book in all_books]

    # Create a user-book matrix
    user_order_matrix = np.zeros((len(book_ids), len(book_ids)))
    for order in orders:
        user_order_matrix[order.book_id - 1][order.book_id - 1] = 1

    # Calculate similarity
    similarity_matrix = cosine_similarity(user_order_matrix)

    # Find similar books
    similar_books = {}
    for order in orders:
        book_id = order.book_id
        for idx, similarity in enumerate(similarity_matrix[book_id - 1]):
            if book_ids[idx] != book_id:
                similar_books[book_ids[idx]] = similar_books.get(book_ids[idx], 0) + similarity

    # Sort and get top recommendations
    recommended_books = sorted(similar_books.items(), key=lambda x: x[1], reverse=True)
    return [book_id for book_id, _ in recommended_books[:5]]
