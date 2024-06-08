from flask import Blueprint, request, jsonify
from models import Book, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from recommendations import get_recommendations

books_bp = Blueprint('books_bp', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = Book.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page,
        'per_page': books.per_page,
        'books': [book.to_dict() for book in books.items]
    })

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@books_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        price=data['price'],
        stock=data['stock'],
        description=data.get('description', '')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@books_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def recommendations():
    user_identity = get_jwt_identity()
    recommended_books = get_recommendations(user_identity['id'])
    books = Book.query.filter(Book.id.in_(recommended_books)).all()
    return jsonify([book.to_dict() for book in books])

@books_bp.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    author = request.args.get('author', '')

    books_query = Book.query
    if query:
        books_query = books_query.filter(Book.title.ilike(f'%{query}%'))
    if genre:
        books_query = books_query.filter_by(genre=genre)
    if author:
        books_query = books_query.filter_by(author=author)

    books = books_query.all()
    return jsonify([book.to_dict() for book in books])
