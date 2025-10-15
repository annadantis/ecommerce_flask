from flask import Blueprint, request, jsonify
from db.connection import get_connection

category_bp = Blueprint('category_bp', __name__)

# List categories
@category_bp.route('/', methods=['GET'])
def get_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categories)

# Add category (admin)
@category_bp.route('/add', methods=['POST'])
def add_category():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (category_name, description) VALUES (%s, %s)",
                   (data['category_name'], data.get('description', '')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Category added successfully!'})
