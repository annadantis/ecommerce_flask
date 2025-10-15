from flask import Blueprint, request, jsonify
from db.connection import get_connection

cart_bp = Blueprint('cart_bp', __name__)

# Add product to cart
@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not user_id or not product_id:
        return jsonify({'error': 'user_id and product_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check if item already exists in cart
    cursor.execute("SELECT * FROM cart_items WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    item = cursor.fetchone()

    if item:
        # Update quantity
        cursor.execute("UPDATE cart_items SET quantity=quantity+%s WHERE user_id=%s AND product_id=%s",
                       (quantity, user_id, product_id))
    else:
        # Insert new item
        cursor.execute("INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (user_id, product_id, quantity))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Product added to cart successfully!'})

# View cart items
@cart_bp.route('/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.cart_id, p.name, p.price, c.quantity, (p.price * c.quantity) AS total
        FROM cart_items c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))

    cart = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(cart)
