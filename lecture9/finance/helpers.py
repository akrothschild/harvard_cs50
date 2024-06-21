import csv
import datetime
import pytz
import requests
import urllib
import uuid
#import yfinance as yf

from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        price = round(float(quotes[-1]["Adj Close"]), 2)
        return {"price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def register():
    """Register user."""

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted and matches
        confirmation = request.form.get("confirmation")
        if not confirmation or password != confirmation:
            return apology("passwords must match", 400)

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
        except ValueError:
            return apology(f"username {username} already exists", 403)

        # Redirect user to login page
        return redirect("/login")

    else:
        return render_template("register.html")


def buy():
    """Buy shares of stock."""

    if request.method == "POST":
        # Ensure symbol was submitted and valid
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 403)

        # Ensure shares were submitted and valid
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("must provide valid number of shares", 403)
        except ValueError:
            return apology("must provide valid number of shares", 403)

        # Lookup the current price of the stock
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 403)

        # Calculate total cost
        total_cost = quote["price"] * shares

        # Ensure user can afford the purchase
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if len(rows) != 1 or rows[0]["cash"] < total_cost:
            return apology("can't afford", 403)

        # Record the purchase in transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, ?)",
                   user_id, quote["symbol"], shares, quote["price"], datetime.datetime.now(pytz.timezone("US/Eastern")))

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        # Redirect user to homepage
        return redirect("/")

    else:
        return render_template("buy.html")


def sell():
    """Sell shares of stock."""

    if request.method == "POST":
        # Ensure symbol was submitted and valid
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("must provide symbol", 403)

        # Ensure shares were submitted and valid
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("must provide valid number of shares", 403)
        except ValueError:
            return apology("must provide valid number of shares", 403)

        # Lookup the current price of the stock
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 403)

        # Determine how many shares the user owns
        user_id = session["user_id"]
        rows = db.execute("SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        if len(rows) != 1 or rows[0]["total_shares"] is None or rows[0]["total_shares"] < shares:
            return apology("don't own enough shares", 403)

        # Calculate total sale value
        total_sale = quote["price"] * shares

        # Record the sale in transactions table (negative shares)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, ?)",
                   user_id, quote["symbol"], -shares, quote["price"], datetime.datetime.now(pytz.timezone("US/Eastern")))

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)

        # Redirect user to homepage
        return redirect("/")

    else:
        return render_template("sell.html")



# def build_graph(symbol):
#     """Look up quote and historical data for symbol."""
#     try:
#         # Fetch data using yfinance
#         stock = yf.Ticker(symbol)
#
#         # Get current price
#         price = stock.history(period='1d')['Close'].iloc[-1]
#
#         # Get historical data for the last 30 days
#         historical_data = stock.history(period='1mo')['Close']
#         dates = historical_data.index.strftime('%Y-%m-%d').tolist()
#         prices = historical_data.tolist()
#
#         return {"symbol": symbol, "price": price, "name": stock.info.get("longName", symbol), "dates": dates, "prices": prices}
#     except Exception:
#         return None


def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure symbol was submitted and valid
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("must provide symbol", 403)

        # Lookup the current price of the stock
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 403)

        # Render quoted price
        return render_template("quote.html", quote=quote)

    else:
        return render_template("quote.html")


def history():
    """Show history of transactions."""

    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC", user_id)

    return render_template("history.html", transactions=transactions)

def login_helper():
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")

def index_helper(db):
    """Show portfolio of stocks"""

    # Check if user_id is in session
    if "user_id" not in session:
        return apology("Unauthorized", 403)

    # Get user's cash balance
    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    # Get user's stock portfolio
    rows = db.execute("""
        SELECT symbol, SUM(shares) as shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
    """, session["user_id"])

    portfolio = []
    total_value = cash

    for row in rows:
        if row["shares"] > 0:
            stock = lookup(row["symbol"])
            if stock:
                total_stock_value = row["shares"] * stock["price"]
                total_value += total_stock_value
                portfolio.append({
                    "symbol": row["symbol"],
                    "shares": row["shares"],
                    "price": stock["price"],
                    "total": total_stock_value
                })

    return render_template("index.html", cash=cash, portfolio=portfolio, total_value=total_value)
