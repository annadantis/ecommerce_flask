from flask import Blueprint, request, jsonify
from db.connection import get_connection

order_bp = Blueprint('order_bp', __name__)

# Create an order from cart
@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get items in cart
    cursor.execute("""
        SELECT c.product_id, c.quantity, p.price
        FROM cart_items c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()
    if not items:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Cart is empty'}), 400

    # Calculate total
    total_amount = sum(item['price'] * item['quantity'] for item in items)

    # Insert order
    cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, total_amount))
    order_id = cursor.lastrowid

    # Insert order items
    for item in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item['product_id'], item['quantity'], item['price']))

    # Clear cart
    cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Order created successfully!', 'order_id': order_id})

# View user's orders
@order_bp.route('/<int:user_id>', methods=['GET'])
def view_orders(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.order_id, o.total_amount, o.status, o.created_at,
               GROUP_CONCAT(CONCAT(p.name, ' x', oi.quantity)) AS items
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.user_id = %s
        GROUP BY o.order_id
        ORDER BY o.created_at DESC
    """, (user_id,))

    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(orders)
