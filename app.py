from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.secret_key = 'your_super_secret_key_123'

# Import routes
from routes.users import user_bp
from routes.products import product_bp
from routes.cart import cart_bp
from routes.orders import order_bp

from routes.categories import category_bp
from routes.admin_products import admin_product_bp


# Register Blueprints
app.register_blueprint(admin_product_bp, url_prefix='/admin/products')

app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(category_bp, url_prefix='/categories')


app.register_blueprint(order_bp, url_prefix='/orders')



app.register_blueprint(user_bp, url_prefix='/users')

app.register_blueprint(cart_bp, url_prefix='/cart')


if __name__ == '__main__':
    app.run(debug=True)
