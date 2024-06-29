import urllib.parse
import requests

from flask import redirect, render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps

'''
========================
=========START==========
========================
'''

'''
========================
DEFINE GLOBAL VARIABLES
========================
'''
alert_start = '<div class="alert alert-info" role="alert">'
alert_end = '</div>'

'''
========================
GENERATE APOLOGY
A function to render an apology.html
========================
'''


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

    if isinstance(message, str):
        message = escape(message)
    else:
        message = "Error occured!"

    return render_template("apology.html", top=code, bottom=message), code


'''
========================
REQUIRE LOGIN
========================
'''


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function


'''
========================
GET STOCKS FROM YAHOO
A function to search and 
return stock info
========================
'''


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
        return {"name": symbol, "price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None


'''
========================
GENERATE ENVIRONMENT
A function to fill 
environmental variables
========================
'''


def usd(value):
    """Format value as USD."""

    return f"${value:,.2f}"


'''
========================
GENERATE TIME
========================
'''


def get_time():
    """Returns formatted local time."""

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


'''
========================
CHECK PASSWORD
========================
'''


def check_password(first_password, second_password):
    """Checks the passwords to be a match. Returns a message error if they do not match."""

    if not check_password_hash(first_password, second_password):
        return apology("Passwords do not match!", code=401)


'''
========================
HELP TO LOGIN
If unsuccessfully return apology.html
========================
'''


def login_helper(db, request):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Query database for username
    rows = db.execute(
        "SELECT * FROM users WHERE username = ?", request.form.get("username")
    )

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
    ):
        return apology("invalid username and/or password", 400)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")


'''
========================
GENERATE CASH
A function to add cash
========================
'''


def cash_helper(db, request):
    user_id = session["user_id"]
    add_cash = request.form.get("add_cash")
    password = request.form.get("password")
    if not password:
        return apology("Must Provide Password", 400)
    if not add_cash:
        return apology("Must Provide Cash to add", 400)
    add_cash = float(add_cash)
    hash_db = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
    if not check_password_hash(hash_db[0]["hash"], password):
        return apology("Incorrect Password!", 400)
    if add_cash > 10000:
        return apology("Cannot add more than $10,000 once", 400)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    db.execute("UPDATE users SET cash = ? + ? WHERE id = ?",
               cash_db[0]["cash"], add_cash, user_id)
    flash("Cash Added!")
    return redirect("/")


'''
========================
CHANGE PASSWORD
========================
'''


def change_password_helper(db, request):
    password = request.form.get("password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    user_id = session["user_id"]
    if not password:
        return apology("Must Provide Password!", 400)
    elif not new_password:
        return apology("Must Provide New Password!", 400)
    elif not confirm_password:
        return apology("Must Confirm New Password!", 400)
    user_data = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
    hash_old = user_data[0]["hash"]
    if not check_password_hash(hash_old, password):
        return apology("Incorrect Password!")
    if new_password != confirm_password:
        return apology("Invalid Confirmation!", 400)
    if new_password == password:
        return apology("New Password is same as your password", 400)
    special_characters = '!@#$%^&*()-+?_=,<>/"'
    if not any(c in special_characters for c in new_password):
        return apology("Password Must Contain a special Character", 400)
    elif not any(c.isalnum() for c in new_password):
        return apology("Password must contain letters and numbers", 400)
    new_hash = generate_password_hash(new_password)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)
    flash("Password Changed!")
    return redirect("/")


'''
========================
GENERATE SALES
A function to sell stocks from one´s portfolio
========================
'''


def sell_helper(db, request):
    symbol = request.form.get("symbol")
    shares = int(request.form.get("shares"))
    if not symbol:
        return apology("Must provide Symbol", 400)
    elif not shares:
        return apology("Must provide number of shares", 400)
    symbol = symbol.upper()
    stock = lookup(symbol)
    if stock == None:
        return apology("Symbol Does not exist")
    if shares < 0:
        return apology("Share not allowed, must be positive integer")
    transaction_value = shares * stock["price"]
    user_id = session["user_id"]
    existing_shares_db = db.execute(
        "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id,
        symbol)
    existing_shares = existing_shares_db[0]["shares"]
    if shares > existing_shares:
        return apology("Too many shares!", 400)
    user_cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash = user_cash_balance[0]["cash"]
    updated_cash = user_cash + transaction_value
    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
    db.execute(
        "INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, ?)", user_id, symbol,
        (-1 * shares), stock["price"], get_time())
    flash("Sold!")
    return redirect("/")


'''
========================
GENERATE REGISTRATION
A function to register a user to use our system
========================
'''


def register_helper(db, request):
    username = request.form.get("username")
    username = username.strip()
    password = request.form.get("password")
    confirm_password = request.form.get("confirmation")
    if confirm_password != password:
        return apology("Invalid Password, password must be same", 400)
    elif not username:
        return apology("must provide username", 400)
    elif not password:
        return apology("must provide password", 400)
    elif not confirm_password:
        return apology("Must Confirm Password!", 400)
    special_characters = '!@#$%^&*()-+?_=,<>/"'
    if not any(c in special_characters for c in password):
        return apology("Password Must Contain a special Character", 400)
    elif not any(c.isalnum() for c in password):
        return apology("Password must contain letters and numbers", 400)
    hash = generate_password_hash(password)
    try:
        # Add username to the database
        db.execute("INSERT INTO users (username, hash) VALUES( ?, ?)", username, hash)
    except:
        return apology("Username Already Exists")
    redirect_message = 'Successfully registered! Login now'
    return render_template("login.html", register_message=redirect_message, alert_start=alert_start,
                           alert_end=alert_end)


'''
========================
GENERATE STOCKS
A function to search for Stocks
========================
'''


def quote_helper(request):
    symbol = request.form.get("symbol")
    symbol = symbol.upper()
    stock = lookup(symbol)
    if stock == None:
        return apology("Symbol Does not exist")
    return render_template("quoted.html", symbol=stock["symbol"], price=stock["price"], alert_start=alert_start,
                           alert_end=alert_end)


'''
========================
GENERATE HISTORY
A function to render an history.html
with all transactions made
========================
'''


def history_helper(db):
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions)


'''
========================
GENERATE PURCHASES
A function to "buy" stocks
========================
'''


def buy_helper(db, request):
    symbol = request.form.get("symbol")
    try:
        shares = int(request.form.get("shares"))
    except ValueError:
        return apology("Share not allowed, must be a positive integer", 400)
    if not symbol:
        return apology("Must provide Symbol", 400)
    elif not shares:
        return apology("Must provide number of shares", 400)
    symbol = symbol.upper()
    stock = lookup(symbol)
    if stock == None:
        return apology("Symbol Does not exist", 400)
    if shares < 0 or not isinstance(shares, int):
        return apology("Share not allowed, must be positive integer", 400)
    user_id = session["user_id"]
    transaction_value = shares * stock["price"]
    user_cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash = user_cash_balance[0]["cash"]
    if user_cash < transaction_value:
        return apology("Cannot afford")
    updated_cash = user_cash - transaction_value
    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price,  transacted) VALUES (?, ?, ?, ?, ?)", user_id,
               symbol, shares, stock["price"], get_time())
    flash("Bought!")
    return redirect("/")


'''
========================
index_helper
Renders index.html with data from DB
========================
'''


def index_helper(db):
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price, SUM(shares)*price AS balance FROM transactions WHERE user_id = ? GROUP BY symbol",
        user_id)
    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]
    cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_balance[0]["cash"]
    total_transactions = db.execute(
        "SELECT SUM(total_balance) AS total FROM (SELECT SUM(shares) * price AS total_balance from transactions WHERE user_id = ? GROUP BY symbol)",
        user_id)
    total = total_transactions[0]["total"]
    if not total:
        total = 0
    total = total + cash
    return render_template("index.html", transactions=transactions, cash=cash, total=total,
                           username=username)


'''
========================
==========END===========
========================
'''
