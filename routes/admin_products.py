from flask import Blueprint, request, jsonify
from db.connection import get_connection

admin_product_bp = Blueprint('admin_product_bp', __name__)

@admin_product_bp.route('/add', methods=['POST'])
def add_product():
    # admin product logic here
    return jsonify({'message': 'Product added!'})
