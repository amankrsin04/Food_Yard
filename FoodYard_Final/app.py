from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "foodyard-college-project-key-change-me"

BASE_DIR = Path(__file__).resolve().parent
DB = str(BASE_DIR / "foodyard.db")


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'donor'
                CHECK(role IN ('donor','admin'))
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS donations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            address TEXT NOT NULL,
            food_date TEXT NOT NULL,
            note TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    admin = conn.execute(
        "SELECT id FROM users WHERE email=?",
        ("admin@foodyard.com",)
    ).fetchone()

    if not admin:
        conn.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (
                "FoodYard Admin",
                "admin@foodyard.com",
                generate_password_hash("admin123"),
                "admin"
            )
        )
    else:
        # Keep the demo admin credentials usable even when an older
        # foodyard.db is already present in the project folder.
        conn.execute(
            "UPDATE users SET name=?, password=?, role=? WHERE email=?",
            (
                "FoodYard Admin",
                generate_password_hash("admin123"),
                "admin",
                "admin@foodyard.com"
            )
        )

    conn.commit()
    conn.close()


def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login first.", "error")
                return redirect(
                    url_for("admin_login" if role == "admin" else "donor_login")
                )

            if role and session.get("role") != role:
                flash("You do not have permission to open that page.", "error")
                return redirect(url_for("dashboard"))

            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year,
        "logged_in": "user_id" in session,
        "current_role": session.get("role"),
        "current_name": session.get("name")
    }


@app.route("/")
def home():
    conn = get_db()
    total_donations = conn.execute(
        "SELECT COUNT(*) AS total FROM donations"
    ).fetchone()["total"]
    total_food = conn.execute(
        "SELECT COALESCE(SUM(quantity),0) AS kg FROM donations"
    ).fetchone()["kg"]
    completed = conn.execute(
        "SELECT COUNT(*) AS total FROM donations WHERE status='Completed'"
    ).fetchone()["total"]
    conn.close()

    return render_template(
        "index.html",
        total_donations=total_donations,
        total_food=total_food,
        completed=completed
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "error")
            return redirect(url_for("register"))

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                (name, email, generate_password_hash(password), "donor")
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        conn.close()
        flash("Donor account created successfully. Please login.", "success")
        return redirect(url_for("donor_login"))

    return render_template("register.html")


def do_login(expected_role):
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        ).fetchone()
        conn.close()

        if (
            user
            and user["role"] == expected_role
            and check_password_hash(user["password"], password)
        ):
            session.clear()
            session.update(
                user_id=user["id"],
                name=user["name"],
                role=user["role"]
            )
            flash(
                "Welcome back, {}!".format(user["name"]),
                "success"
            )
            return redirect(url_for("dashboard"))

        flash(
            "Invalid {} email or password.".format(expected_role),
            "error"
        )

    return render_template(
        "login.html",
        login_type=expected_role,
        login_action=url_for(
            "admin_login" if expected_role == "admin" else "donor_login"
        )
    )


@app.route("/login")
def login():
    return redirect(url_for("donor_login"))


@app.route("/donor/login", methods=["GET", "POST"])
def donor_login():
    return do_login("donor")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    return do_login("admin")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required()
def dashboard():
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("donor_dashboard"))


@app.route("/donor/dashboard")
@login_required("donor")
def donor_dashboard():
    conn = get_db()
    donations = conn.execute(
        "SELECT * FROM donations WHERE user_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()

    stats = conn.execute("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(quantity),0) AS kg,
            SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) AS pending
        FROM donations
        WHERE user_id=?
    """, (session["user_id"],)).fetchone()

    conn.close()
    return render_template(
        "dashboard.html",
        donations=donations,
        stats=stats
    )


@app.route("/donate", methods=["GET", "POST"])
@login_required("donor")
def donate():
    if request.method == "POST":
        food_type = request.form.get("food_type", "").strip()
        address = request.form.get("address", "").strip()
        food_date = request.form.get("food_date", "").strip()
        note = request.form.get("note", "").strip()

        try:
            quantity = float(request.form.get("quantity", "0"))
        except ValueError:
            quantity = 0

        if not food_type or not address or not food_date or quantity <= 0:
            flash("Please enter valid donation details.", "error")
            return redirect(url_for("donate"))

        conn = get_db()
        conn.execute("""
            INSERT INTO donations
            (user_id,food_type,quantity,address,food_date,note,status,created_at)
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            session["user_id"],
            food_type,
            quantity,
            address,
            food_date,
            note,
            "Pending",
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()

        flash("Food donation submitted successfully!", "success")
        return redirect(url_for("donor_dashboard"))

    return render_template("donate.html")


@app.route("/admin/dashboard")
@login_required("admin")
def admin_dashboard():
    conn = get_db()

    donations = conn.execute("""
        SELECT d.*, u.name AS donor, u.email AS donor_email
        FROM donations d
        JOIN users u ON u.id=d.user_id
        ORDER BY d.id DESC
    """).fetchall()

    stats = conn.execute("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(quantity),0) AS kg,
            SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status='Accepted' THEN 1 ELSE 0 END) AS accepted,
            SUM(CASE WHEN status='Collected' THEN 1 ELSE 0 END) AS collected
        FROM donations
    """).fetchone()

    donors = conn.execute("""
        SELECT id, name, email
        FROM users
        WHERE role='donor'
        ORDER BY id DESC
    """).fetchall()

    messages = conn.execute("""
        SELECT * FROM contact_messages
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        donations=donations,
        stats=stats,
        donors=donors,
        messages=messages
    )


@app.route("/admin/status/<int:donation_id>", methods=["POST"])
@login_required("admin")
def update_status(donation_id):
    status = request.form.get("status", "")
    allowed = {
        "Pending",
        "Accepted",
        "Collected",
        "Distributed",
        "Completed",
        "Rejected"
    }

    if status not in allowed:
        flash("Invalid status.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db()
    conn.execute(
        "UPDATE donations SET status=? WHERE id=?",
        (status, donation_id)
    )
    conn.commit()
    conn.close()

    flash("Donation status updated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill all contact fields.", "error")
            return redirect(url_for("contact"))

        conn = get_db()
        conn.execute("""
            INSERT INTO contact_messages(name,email,message,created_at)
            VALUES(?,?,?,?)
        """, (
            name,
            email,
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()

        flash("Thank you! Your message has been received.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
