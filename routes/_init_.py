from flask import Blueprint, request, jsonify
from db.connection import get_connection

admin_product_bp = Blueprint('admin_product_bp', __name__)

@admin_product_bp.route('/admin/products/add', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']
    stock = data['stock_quantity']
    category_id = data['category_id']
    image_url = data['image_url']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, description, price, stock, category_id, image_url))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Product added successfully!'})

@admin_product_bp.route('/admin/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product deleted successfully!'})

@admin_product_bp.route('/admin/products/update/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data['name']
    price = data['price']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=%s, price=%s WHERE product_id=%s", (name, price, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product updated successfully!'})
