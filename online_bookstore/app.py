from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.books import books_bp
from routes.orders import orders_bp
from routes.wishlist import wishlist_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///online_bookstore.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

@app.route('/')
def home():
    return "Welcome to the Online Bookstore API"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
