from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory database
books_db = []
next_id = 1

@app.route('/api/books', methods=['GET', 'POST'])
def books():
    global next_id
    if request.method == 'POST':
        book = request.json
        book['id'] = next_id
        book['status'] = 'available'
        books_db.append(book)
        next_id += 1
        return jsonify(book), 201
    return jsonify(books_db)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = [b for b in books_db if query in str(b).lower()]
    return jsonify(results)

@app.route('/api/borrow', methods=['POST'])
def borrow():
    data = request.json
    for book in books_db:
        if book['isbn'] == data['isbn'] and book['status'] == 'available':
            book['status'] = 'borrowed'
            book['borrower'] = data['borrower']
            book['borrow_date'] = data['date']
            book['return_date'] = data['return_date']
            return jsonify(book)
    return jsonify({'error': 'Book not available'}), 400

@app.route('/api/return', methods=['POST'])
def return_book():
    isbn = request.json['isbn']
    for book in books_db:
        if book['isbn'] == isbn and book['status'] == 'borrowed':
            book['status'] = 'available'
            book.pop('borrower', None)
            book.pop('borrow_date', None)
            book.pop('return_date', None)
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

@app.route('/api/borrowed')
def borrowed():
    return jsonify([b for b in books_db if b['status'] == 'borrowed'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
