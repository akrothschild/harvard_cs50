from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

import helpers

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = helpers.usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@helpers.login_required
def index():
    """Show portfolio of stocks"""
    return helpers.index_helper(db)


@app.route("/buy", methods=["GET", "POST"])
@helpers.login_required
def buy_route():
    """Buy shares of stock"""
    if request.method == "POST":
        return helpers.buy_helper(db, request)
    else:
        return render_template("buy.html")


@app.route("/history")
@helpers.login_required
def history_route():
    """Show history of transactions"""
    return helpers.history_helper(db)


@app.route("/login", methods=["GET", "POST"])
def login_route():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        return helpers.login_helper(db, request)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout_route():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@helpers.login_required
def quote_route():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif not request.form.get("symbol"):
        return helpers.apology("Must Provide Symbol", 400)
    else:
        return helpers.quote_helper(request)


@app.route("/register", methods=["GET", "POST"])
def register_route():
    """Register user"""
    session.clear()
    if request.method == "POST":
        return helpers.register_helper(db, request)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@helpers.login_required
def sell_route():
    """Sell shares of stock"""
    if request.method == "POST":
        return helpers.sell_helper(db, request)
    else:
        user_id = session["user_id"]
        user_symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", user_symbols=user_symbols)


@app.route("/change-password", methods=["GET", "POST"])
@helpers.login_required
def change_password_route():
    if request.method == "POST":
        return helpers.change_password_helper(db, request)
    else:
        return render_template("change-password.html")


@app.route("/add-cash", methods=["GET", "POST"])
@helpers.login_required
def cash_route():
    if request.method == "POST":
        return helpers.cash_helper(db, request)
    else:
        return render_template("add-cash.html")
