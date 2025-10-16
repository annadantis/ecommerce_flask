from flask import Blueprint, request, jsonify
from db.connection import get_connection

cart_bp = Blueprint('cart_bp', __name__)

# 🛒 ADD PRODUCT TO CART
@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.json or {}
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not user_id or not product_id:
        return jsonify({'error': '❌ user_id and product_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.start_transaction()

        # Lock product row
        cursor.execute("SELECT stock_quantity FROM products WHERE product_id=%s FOR UPDATE", (product_id,))
        product = cursor.fetchone()
        if not product:
            conn.rollback()
            return jsonify({'error': '❌ Product not found'}), 404

        stock = product[0]
        if stock < quantity:
            conn.rollback()
            return jsonify({'error': '⚠️ Insufficient stock'}), 400

        # Check existing item in cart
        cursor.execute("SELECT quantity FROM cart_items WHERE user_id=%s AND product_id=%s FOR UPDATE",
                       (user_id, product_id))
        item = cursor.fetchone()

        if item:
            cursor.execute(
                "UPDATE cart_items SET quantity = quantity + %s WHERE user_id=%s AND product_id=%s",
                (quantity, user_id, product_id)
            )
        else:
            cursor.execute(
                "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                (user_id, product_id, quantity)
            )

        # Reduce stock
        cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s", (quantity, product_id))

        conn.commit()
        return jsonify({'message': '✅ Product added to cart successfully!'})

    except Exception as e:
        conn.rollback()
        print("Error adding to cart:", e)
        return jsonify({'error': 'Server error while adding to cart.'}), 500

    finally:
        cursor.close()
        conn.close()


# 🧾 VIEW CART ITEMS
@cart_bp.route('/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.cart_id, c.product_id, p.name, p.price, c.quantity, (p.price * c.quantity) AS total
        FROM cart_items c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = %s
    """, (user_id,))

    cart = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(cart)



# ❌ REMOVE ITEM / DECREASE QUANTITY
@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    data = request.json or {}
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not user_id or not product_id:
        return jsonify({'error': '❌ user_id and product_id are required'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.start_transaction()

        # Check if item in cart
        cursor.execute("SELECT quantity FROM cart_items WHERE user_id=%s AND product_id=%s FOR UPDATE",
                       (user_id, product_id))
        item = cursor.fetchone()

        if not item:
            conn.rollback()
            return jsonify({'error': '⚠️ Item not found in cart'}), 404

        current_qty = item[0]

        if current_qty <= quantity:
            # Remove item completely
            cursor.execute("DELETE FROM cart_items WHERE user_id=%s AND product_id=%s",
                           (user_id, product_id))
            qty_to_restore = current_qty
        else:
            # Reduce quantity
            cursor.execute("UPDATE cart_items SET quantity = quantity - %s WHERE user_id=%s AND product_id=%s",
                           (quantity, user_id, product_id))
            qty_to_restore = quantity

        # Restore product stock
        cursor.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id=%s",
                       (qty_to_restore, product_id))

        conn.commit()
        return jsonify({'message': '🗑️ Item removed from cart successfully!'})

    except Exception as e:
        conn.rollback()
        print("Error removing from cart:", e)
        return jsonify({'error': 'Server error while removing item.'}), 500

    finally:
        cursor.close()
        conn.close()
