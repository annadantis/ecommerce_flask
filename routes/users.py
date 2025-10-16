from flask import Blueprint, request, jsonify, session
from db.connection import get_connection
import bcrypt

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
    # Set session info
        session['user_id'] = user['user_id']
        session['role'] = user['role']  # 'admin' or 'customer'
    
        return jsonify({
            'message': 'Login successful!',
            'user': {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash,role)
            VALUES (%s, %s, %s,%s)
        """, (username, email, password_hash,'customer'))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()
