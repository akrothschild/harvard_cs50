import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import apology, login_required, lookup, usd, register, buy, sell, quote, history, login_helper, \
    index_helper

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def create_tables():
    """Create tables if they do not exist."""
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL,
                cash NUMERIC NOT NULL DEFAULT 10000.00
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                price NUMERIC NOT NULL,
                transacted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("Tables created successfully or already exist.")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Create tables if they do not exist
create_tables()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    create_tables()
    """Show portfolio of stocks"""
    if request.method == "GET":
        return index_helper(db, request)
    else:
        return apology("no stocks here", 403)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy_route():
    """Buy shares of stock"""
    if request.method == "POST":
        return buy()
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history_route():
    """Show history of transactions"""
    return history()


@app.route("/login", methods=["GET", "POST"])
def login(response):
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        response.status_code = 200
        return login_helper()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote_route():
    """Get stock quote."""
    if request.method == "POST":
        return quote()
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register_route():
    """Register user"""
    if request.method == "POST":
        return register()
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell_route():
    """Sell shares of stock"""
    if request.method == "POST":
        return sell()
    else:
        return render_template("sell.html")


if __name__ == "__main__":
    app.run(debug=True)
