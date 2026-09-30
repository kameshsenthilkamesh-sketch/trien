from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "canteen_secret_key"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("canteen.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Order Received'
        )
    """)

    # Add sample food only if menu is empty
    count = conn.execute("SELECT COUNT(*) FROM menu").fetchone()[0]

    if count == 0:
        foods = [
            ("Veg Sandwich", 40),
            ("Burger", 60),
            ("Pizza", 80),
            ("Noodles", 50),
            ("Fried Rice", 60),
            ("Tea", 15),
            ("Coffee", 20),
            ("Dosa", 35)
        ]

        conn.executemany(
            "INSERT INTO menu (name, price) VALUES (?, ?)",
            foods
        )

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MENU ----------------

@app.route("/menu")
def menu():
    conn = get_db()
    foods = conn.execute(
        "SELECT * FROM menu WHERE available = 1"
    ).fetchall()
    conn.close()

    return render_template("menu.html", foods=foods)


# ---------------- PLACE ORDER ----------------

@app.route("/place_order", methods=["POST"])
def place_order():

    items = request.form["items"]
    total = request.form["total"]

    order_id = "KPR" + str(random.randint(1000, 9999))

    conn = get_db()

    conn.execute("""
        INSERT INTO orders
        (order_id, items, total)
        VALUES (?, ?, ?)
    """, (order_id, items, total))

    conn.commit()
    conn.close()

    return redirect(url_for("order_success", order_id=order_id))


# ---------------- ORDER SUCCESS ----------------

@app.route("/order/<order_id>")
def order_success(order_id):

    conn = get_db()

    order = conn.execute(
        "SELECT * FROM orders WHERE order_id = ?",
        (order_id,)
    ).fetchone()

    conn.close()

    return render_template("order.html", order=order)


# ---------------- TRACK ORDER ----------------

@app.route("/track/<order_id>")
def track_order(order_id):

    conn = get_db()

    order = conn.execute(
        "SELECT * FROM orders WHERE order_id = ?",
        (order_id,)
    ).fetchone()

    conn.close()

    return render_template("track.html", order=order)


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
