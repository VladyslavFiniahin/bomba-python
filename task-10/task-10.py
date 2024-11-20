from flask import Flask, jsonify, request, abort
import csv
import os

app = Flask(__name__)

CSV_FILE = 'books.csv'

def read_books():
    books = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

def write_books(books):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'author', 'year', 'genre'])
        writer.writeheader()
        writer.writerows(books)

@app.route('/books', methods=['GET'])
def get_books():
    books = read_books()
    return jsonify(books), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    books = read_books()
    book = next((b for b in books if int(b['id']) == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book), 200

@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not all(k in request.json for k in ['title', 'author', 'year', 'genre']):
        abort(400, description="Invalid data")
    books = read_books()
    new_id = max(int(b['id']) for b in books) + 1 if books else 1
    new_book = {
        'id': str(new_id),
        'title': request.json['title'],
        'author': request.json['author'],
        'year': str(request.json['year']),
        'genre': request.json['genre']
    }
    books.append(new_book)
    write_books(books)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.json:
        abort(400, description="Invalid data")
    books = read_books()
    book = next((b for b in books if int(b['id']) == book_id), None)
    if not book:
        abort(404, description="Book not found")
    for key in ['title', 'author', 'year', 'genre']:
        if key in request.json:
            book[key] = request.json[key]
    write_books(books)
    return jsonify(book), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = read_books()
    book = next((b for b in books if int(b['id']) == book_id), None)
    if not book:
        abort(404, description="Book not found")
    books = [b for b in books if int(b['id']) != book_id]
    write_books(books)
    return jsonify({'message': 'Book deleted successfully'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'title', 'author', 'year', 'genre'])
            writer.writeheader()
    app.run(debug=True)
