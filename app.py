from flask import Flask, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy user database
users = {}

# Menu items with working image URLs
menu_items = [
    {"id": 1, "name": "Pizza", "price": 12.99, "image": "https://www.foodandwine.com/thmb/Wd4lBRZz3X_8qBr69UOu2m7I2iw=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/classic-cheese-pizza-FT-RECIPE0422-31a2c938fc2546c9a07b7011658cfd05.jpg"},
    {"id": 2, "name": "Burger", "price": 8.99, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/RedDot_Burger.jpg/1200px-RedDot_Burger.jpg"},
    {"id": 3, "name": "Pasta", "price": 10.49, "image": "https://s.lightorangebean.com/media/20240914160809/Spicy-Penne-Pasta_-done.png"},
    {"id": 4, "name": "Fries", "price": 5.99, "image": "https://www.awesomecuisine.com/wp-content/uploads/2009/05/french-fries.jpg"},
]

orders = []


# ---------- HOME ----------
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('menu'))
    return login_page()


# ---------- LOGIN PAGE ----------
def login_page(message=""):
    return f"""
    <html>
    <head>
    <title>Food Delivery System</title>
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f0f2f5, #d9e4ec);
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0;
        }}
        .container {{
            background: white;
            padding: 40px 50px;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            text-align: center;
            width: 350px;
        }}
        h1 {{
            color: #2C3E50;
            margin-bottom: 20px;
        }}
        input {{
            width: 90%; padding: 10px; margin: 10px 0;
            border: 1px solid #ccc; border-radius: 8px;
        }}
        button {{
            background-color: #0056b3; color: white;
            padding: 10px 25px; border: none;
            border-radius: 8px; cursor: pointer;
            font-size: 16px; width: 100%;
        }}
        button:hover {{ background-color: #004090; }}
        a {{
            color: #0056b3; text-decoration: none;
            font-size: 14px;
        }}
        p {{ color: red; }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>Login</h1>
        <p>{message}</p>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <p>New user? <a href="/signup">Create an account</a></p>
    </div>
    </body></html>
    """


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['user'] = username
        return redirect(url_for('menu'))
    return login_page("Invalid username or password!")


# ---------- SIGNUP PAGE ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return signup_page("User already exists!")
        users[username] = password
        return redirect(url_for('home'))
    return signup_page()


def signup_page(message=""):
    return f"""
    <html><head><title>Signup</title>
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #e9eef5, #cbd6e0);
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0;
        }}
        .container {{
            background: white;
            padding: 40px 50px;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            text-align: center;
            width: 350px;
        }}
        h2 {{
            color: #2C3E50;
            margin-bottom: 20px;
        }}
        input {{
            width: 90%; padding: 10px; margin: 10px 0;
            border: 1px solid #ccc; border-radius: 8px;
        }}
        button {{
            background-color: #007bff; color: white;
            padding: 10px 25px; border: none;
            border-radius: 8px; cursor: pointer;
            font-size: 16px; width: 100%;
        }}
        button:hover {{ background-color: #0056b3; }}
        a {{
            color: #007bff; text-decoration: none;
            font-size: 14px;
        }}
        p {{ color: red; }}
    </style>
    </head><body>
    <div class="container">
        <h2>Sign Up</h2>
        <p>{message}</p>
        <form method="POST" action="/signup">
            <input name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Sign Up</button>
        </form>
        <p><a href="/">Back to Login</a></p>
    </div></body></html>
    """


# ---------- MENU ----------
@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('home'))
    items_html = "".join([
        f"""
        <div class='card'>
            <img src='{item["image"]}' alt='{item["name"]}' />
            <h3>{item["name"]}</h3>
            <p>₹{item["price"]}</p>
            <form method='POST' action='/order/{item["id"]}'>
                <button type='submit'>Order</button>
            </form>
        </div>
        """ for item in menu_items
    ])
    return f"""
    <html><head><title>Menu</title>
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: #f7f9fc;
            text-align: center;
            margin: 0;
        }}
        h2 {{ color: #2C3E50; margin-top: 30px; }}
        .menu {{
            display: flex; flex-wrap: wrap; justify-content: center;
            gap: 20px; margin-top: 30px;
        }}
        .card {{
            width: 220px; background: white; padding: 20px;
            border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        img {{ width: 100%; height: 150px; border-radius: 10px; object-fit: cover; }}
        button {{
            background-color: #28a745; color: white; border: none; padding: 10px 20px;
            border-radius: 10px; cursor: pointer; font-size: 16px;
        }}
        button:hover {{ background-color: #218838; }}
        .logout {{ margin: 30px; }}
        a {{ color: #e74c3c; text-decoration: none; font-weight: bold; }}
    </style>
    </head><body>
        <h2>Welcome, {session['user']} 🍽️</h2>
        <div class="menu">{items_html}</div>
        <div class="logout">
            <a href="/logout">Logout</a>
        </div>
    </body></html>
    """


# ---------- ORDER ----------
@app.route('/order/<int:item_id>', methods=['POST'])
def order(item_id):
    if 'user' not in session:
        return redirect(url_for('home'))
    item = next((i for i in menu_items if i['id'] == item_id), None)
    if not item:
        return "Item not found"
    orders.append({"user": session['user'], "item": item})
    return f"""
    <html><body style='text-align:center; font-family:Poppins; background:#f0f2f5;'>
    <h2>✅ Order Confirmed!</h2>
    <p>You ordered <b>{item['name']}</b> for ₹{item['price']}</p>
    <a href="/menu" style="color:#007bff; text-decoration:none;">Back to Menu</a>
    </body></html>
    """


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
