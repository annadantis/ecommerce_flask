import requests

# Register a user (POST request)
register_url = "http://127.0.0.1:5000/users/register"
register_data = {
    "username": "john",
    "email": "john@example.com",
    "password": "12345"
}

try:
    res = requests.post(register_url, json=register_data)
    print("Register Response:", res.json())
except Exception as e:
    print("Error while registering user:", e)

# Get all products (GET request)
products_url = "http://127.0.0.1:5000/products/"
try:
    res2 = requests.get(products_url)
    print("Products Response:", res2.json())
except Exception as e:
    print("Error while fetching products:", e)



# Login
res = requests.post("http://127.0.0.1:5000/users/login", json={
    "email": "john@example.com",
    "password": "12345"
})
print("Login Response:", res.json())

# Add to cart
res = requests.post("http://127.0.0.1:5000/cart/add", json={
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
})
print("Add to Cart:", res.json())

# View cart
res = requests.get("http://127.0.0.1:5000/cart/1")
print("Cart Items:", res.json())

# Create order
res = requests.post("http://127.0.0.1:5000/orders/create", json={"user_id": 1})
print("Create Order:", res.json())

# View user's orders
res = requests.get("http://127.0.0.1:5000/orders/1")
print("User Orders:", res.json())


# Add a product
res = requests.post("http://127.0.0.1:5000/products/add", json={
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1299.99,
    "stock_quantity": 5,
    "category_id": 1,
    "image_url": "https://example.com/laptop.jpg"
})
print("Add Product:", res.json())

# Edit a product
res = requests.put("http://127.0.0.1:5000/products/edit/1", json={
    "name": "iPhone 15 Pro",
    "description": "Latest Apple iPhone",
    "price": 1099.99,
    "stock_quantity": 15,
    "category_id": 1,
    "image_url": "https://example.com/iphone15pro.jpg"
})
print("Edit Product:", res.json())

# Delete a product
res = requests.delete("http://127.0.0.1:5000/products/delete/2")
print("Delete Product:", res.json())