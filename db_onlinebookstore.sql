-- Database schema for Online Bookstore
CREATE DATABASE IF NOT EXISTS db_onlinebookstore;
USE db_onlinebookstore;

CREATE TABLE authors (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE books (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT,
    book_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

INSERT INTO authors (name) VALUES ('Author One'), ('Author Two');
INSERT INTO books (title, author_id) VALUES ('Book One', 1), ('Book Two', 2);
