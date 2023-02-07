import os
import requests
import urllib.parse

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, error

# Configure application
app = Flask(__name__)

""" 
# Ensure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""

# TO-DO: Initialize database as db with SQLAlchemy
# The db is used as shorthand to access the database
# Old code: db = SQL("sqlite:///finance.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
@login_required
def add():
    return error("This page (add) has not yet been created", 404)

@app.route("/login", methods=["GET", "POST"])
def login():
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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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

@app.route("/overview")
@login_required
def overview():
    return error("This page (overview) has not yet been created", 404)

@app.route("/register", methods=["GET", "POST"])
def register():
        # POST method when form is submitted
    if request.method == "POST":
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        passcheck = str(request.form.get("confirmation"))

        # Get list of usernames
        usernames = db.execute("SELECT username FROM users")

        if username == "":
            return apology("no username")

        name_check = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(name_check) != 0 and name_check[0]["username"] == username:
            return apology("username is already taken")

        if password == "":
            return apology("no password")

        if password != passcheck:
            return apology("passwords don't match")

        # Hash password and register user
        passhash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passhash)

        # Treat the new user as being logged in
        userid_table = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = userid_table[0]["id"]

        flash("You have been registered!")
        return redirect("/")

    else:
        return render_template("register.html")