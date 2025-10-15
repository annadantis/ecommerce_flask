const API_URL = "http://127.0.0.1:5000";

// ======= LOGIN =======
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    document.getElementById("message").innerText = data.message || data.error;

    if (data.user) {
        localStorage.setItem("user_id", data.user.user_id);
        localStorage.setItem("role", data.user.role);
        window.location.href = "products.html";
    }
});

// ======= LOAD PRODUCTS =======
async function loadProducts() {
    const res = await fetch(`${API_URL}/products/`);
    const products = await res.json();
    const container = document.getElementById("products");
    if(!container) return;

    container.innerHTML = "";
    products.forEach(p => {
        container.innerHTML += `
            <h3>${p.name} - $${p.price}</h3>
            <p>${p.description}</p>
            <p>Stock: ${p.stock_quantity}</p>
            <button onclick="addToCart(${p.product_id})">Add to Cart</button><hr>
        `;
    });
}

// ======= CART =======
async function addToCart(product_id) {
    const user_id = localStorage.getItem("user_id");
    if(!user_id) return alert("Login first!");

    const res = await fetch(`${API_URL}/cart/add`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id, product_id, quantity:1})
    });
    const data = await res.json();
    alert(data.message);
}

async function loadCart() {
    const user_id = localStorage.getItem("user_id");
    const container = document.getElementById("cartItems");
    if(!container) return;

    const res = await fetch(`${API_URL}/cart/${user_id}`);
    const cart = await res.json();
    container.innerHTML = "";
    cart.forEach(item => container.innerHTML += `<p>${item.name} x${item.quantity} = $${item.total}</p>`);
}

async function checkout() {
    const user_id = localStorage.getItem("user_id");
    const res = await fetch(`${API_URL}/orders/create`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id})
    });
    const data = await res.json();
    document.getElementById("message").innerText = data.message || data.error;
    loadCart();
}

// ======= ADMIN FUNCTIONS =======

const role = localStorage.getItem("role");

// Admin products page
if(window.location.href.includes("admin.html")) {
    if(role !== "admin") {
        alert("Admins only!");
        window.location.href = "index.html";
    } else {
        loadAdminProducts();
    }
}

// Admin categories page
if(window.location.href.includes("admin_categories.html")) {
    if(role !== "admin") {
        alert("Admins only!");
        window.location.href = "index.html";
    } else {
        loadCategories();
    }
}

// Normal products page (for all logged-in users)
if(window.location.href.includes("products.html")) {
    loadProducts();
}

// Cart page
if(window.location.href.includes("cart.html")) {
    loadCart();
}


// Admin products
async function loadAdminProducts() {
    const res = await fetch(`${API_URL}/products/`);
    const products = await res.json();
    const container = document.getElementById("products");
    if(!container) return;

    container.innerHTML = "";
    products.forEach(p => {
        container.innerHTML += `
            <b>${p.name}</b> - $${p.price} | Stock: ${p.stock_quantity}
            <button onclick="deleteProduct(${p.product_id})">Delete</button><hr>
        `;
    });
}

async function addProduct() {
    const user_id = localStorage.getItem("user_id");
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const price = parseFloat(document.getElementById("price").value);
    const stock = parseInt(document.getElementById("stock").value);
    const category_id = parseInt(document.getElementById("category_id").value);
    const image_url = document.getElementById("image_url").value;

    const res = await fetch(`${API_URL}/admin/products/add`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id, name, description, price, stock_quantity:stock, category_id, image_url})
    });

    const data = await res.json();
    document.getElementById("message").innerText = data.message || data.error;
    loadAdminProducts();
}

async function deleteProduct(product_id) {
    const res = await fetch(`${API_URL}/admin/products/delete/${product_id}`, {method:"DELETE"});
    const data = await res.json();
    alert(data.message);
    loadAdminProducts();
}

// Admin categories
async function loadCategories() {
    const res = await fetch(`${API_URL}/categories/`);
    const categories = await res.json();
    const container = document.getElementById("categories");
    if(!container) return;

    container.innerHTML = "";
    categories.forEach(c => container.innerHTML += `<p>${c.category_name} (ID:${c.category_id})</p>`);
}

async function addCategory() {
    const user_id = localStorage.getItem("user_id");
    const category_name = document.getElementById("category_name").value;
    const description = document.getElementById("category_description").value;

    const res = await fetch(`${API_URL}/categories/add`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id, category_name, description})
    });

    const data = await res.json();
    document.getElementById("catMessage").innerText = data.message || data.error;
    loadCategories();
}

// ======= REGISTER =======
document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const full_name = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, full_name, email, password })
    });

    const data = await res.json();
    document.getElementById("message").innerText = data.message || data.error;

    if(data.message){
        setTimeout(() => {
            window.location.href = "login.html"; // redirect to login after success
        }, 1500);
    }
});


// Load pages
if(document.getElementById("products") && role==="admin") loadAdminProducts();
if(document.getElementById("categories") && role==="admin") loadCategories();
if(document.getElementById("products") && role!=="admin") loadProducts();
if(document.getElementById("cartItems")) loadCart();
