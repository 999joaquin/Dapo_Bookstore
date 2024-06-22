from flask import Flask, request, jsonify, make_response
from database import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Welcome to Author Service"

@app.route("/authors", methods=["GET"])
def get_authors():
    sql = "SELECT * FROM authors"
    data = get_data(query=sql)
    if data:
        authors = [{"id": row[0], "name": row[1]} for row in data]
        return make_response(jsonify({"authors": authors}))
    else:
        return make_response(jsonify({"status": 404, "message": "No authors found"}))

@app.route("/author/<int:id>", methods=["GET"])
def get_author(id):
    sql = f"SELECT * FROM authors WHERE id = {id}"
    data = get_data(query=sql)
    if data:
        author = {"id": data[0][0], "name": data[0][1]}
        return make_response(jsonify(author))
    else:
        return make_response(jsonify({"status": 404, "message": f"Author with id {id} not found"}))

if __name__ == "__main__":
    app.run(port=5002, debug=True)
