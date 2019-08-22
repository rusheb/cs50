import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    assets = db.execute(
        "SELECT symbol, sum(shares) AS sum_shares \
        FROM 'Transaction' \
        WHERE user=:userId \
        GROUP BY symbol \
        HAVING sum_shares <> 0",
        userId=session['user_id']
    )
    cash = db.execute(
        "SELECT cash FROM users where id=:userId",
        userId=session['user_id']
    )

    grand_total = 0
    for stock in assets:
        api_data = lookup(stock['Symbol'])
        for key in api_data:
            stock[key] = api_data[key]

        stock['total'] = stock['price'] * stock['sum_shares']
        grand_total += stock['total']

    return render_template(
        "index.html",
        assets=assets,
        cash=cash[0]['cash'],
        total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("please enter an int", 400)

        if not shares or shares < 0:
            return apology("please enter an amount greater than 0", 400)

        # check the user has entered a a correct symbol with an amount
        if not request.form.get("symbol"):
            return apology("please enter a symbol", 400)

        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("unknown symbol")

        # check the user has enough cash
        rows = db.execute(
            "SELECT cash FROM users WHERE id = :userId",
            userId=session['user_id']
        )

        # todo use shares variable
        cost = stock['price'] * int(request.form.get("shares"))
        cash = rows[0]['cash'] - cost

        if cash < 0:
            return apology("not enough cash")

        # add the transaction to the database
        db.execute("INSERT INTO 'Transaction' (User, Symbol, Shares, PricePerShare) \
                    VALUES (:user, :symbol, :shares, :price)",
                   user=session['user_id'],
                   symbol=stock['symbol'],
                   shares=request.form.get("shares"),
                   price=stock['price']
                   )

        # update the user's cash
        db.execute("UPDATE 'users' SET 'cash' = :cash WHERE id = :userId",
                   cash=cash,
                   userId=session['user_id']
                   )

        return redirect("/")

    elif request.method == "GET":
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute(
        "SELECT * FROM 'Transaction' WHERE user = :userId",
        userId=session['user_id']
    )

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please enter a symbol")

        stock_info = lookup(request.form.get("symbol"))

        if not stock_info:
            return apology("unknown symbol")

        return render_template("quoted.html", stock=stock_info)

    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        user = request.form.get("username")
        pwd = request.form.get("password")
        pwd2 = request.form.get("confirmation")

        if not pwd == pwd2:
            return apology("passwords must match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=user)

        if len(rows) != 0:
            return apology("username already exists")

        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=user,
            hash=generate_password_hash(pwd)
        )

        return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 403)

        if not request.form.get("shares"):
            return apology("must provide password", 403)

        owned = db.execute(
            "SELECT symbol, sum(shares) AS Shares FROM 'Transaction' \
            WHERE user=:userId AND symbol = :symbol \
            GROUP BY symbol",
            userId=session['user_id'],
            symbol=symbol
        )[0]['Shares']

        if owned < int(request.form.get("shares")):
            return apology(f"you only own {owned} {symbol}")

        data = lookup(symbol)

        db.execute("INSERT INTO 'Transaction' (User, Symbol, Shares, PricePerShare) \
                    VALUES (:user, :symbol, :shares, :price)",
                   user=session['user_id'],
                   symbol=symbol,
                   shares=int(request.form.get("shares")) * -1,
                   price=data['price']
                   )

        return redirect("/")

    elif request.method == "GET":
        rows = db.execute(
            "SELECT symbol from 'Transaction' \
            WHERE user = :user \
            GROUP BY symbol \
            HAVING sum(Shares) <> 0",
            user=session['user_id']
        )
        stocks = [stock['Symbol'] for stock in rows]

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
