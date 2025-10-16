from flask import Blueprint, request, jsonify,session,abort
from db.connection import get_connection

admin_product_bp = Blueprint('admin_product_bp', __name__)

@admin_product_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    if not session.get('is_admin'):  # Check if user is admin
        return jsonify({'error': 'Admin only'}), 403  # Forbidden
    # Fetch products or render dashboard
    return jsonify({'message': 'Welcome Admin!'})

# ✅ Add new product
@admin_product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['name'],
            data['description'],
            data['price'],
            data['stock_quantity'],
            data['category_id'],
            data.get('image_url', '')
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': '✅ Product added successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ✅ Get all products (for admin dashboard)
@admin_product_bp.route('/', methods=['GET'])
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ✅ Delete a product by ID
@admin_product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()
        return jsonify({'message': '🗑️ Product deleted successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()
