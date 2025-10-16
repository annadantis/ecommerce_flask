from flask import Blueprint, request, jsonify
from db.connection import get_connection

product_bp = Blueprint('product_bp', __name__)

# List all products
@product_bp.route('/', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id')  # optional

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if category_id:
        cursor.execute("SELECT * FROM products WHERE category_id=%s", (category_id,))
    else:
        cursor.execute("SELECT * FROM products")
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(products)

# Add a new product (admin)
@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['name'],
        data.get('description', ''),
        data['price'],
        data.get('stock_quantity', 0),
        data.get('category_id'),
        data.get('image_url', '')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product added successfully!'})

# Edit a product (admin)
@product_bp.route('/edit/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name=%s, description=%s, price=%s, stock_quantity=%s, category_id=%s, image_url=%s
        WHERE product_id=%s
    """, (
        data['name'],
        data.get('description', ''),
        data['price'],
        data.get('stock_quantity', 0),
        data.get('category_id'),
        data.get('image_url', ''),
        product_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product updated successfully!'})

# Delete a product (admin)
@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product deleted successfully!'})
