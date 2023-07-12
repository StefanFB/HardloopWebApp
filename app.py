import os
import requests
import sqlite3
import urllib.parse
import models

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, select, text, ForeignKey, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from helpers import login_required, error

# Configure application
app = Flask(__name__)

""" 
# Ensure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""

# Create classes for each table in database
class Base(DeclarativeBase):
    pass

class user(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

# The db is used as shorthand to access the database
db = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(db)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configuration of each route
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
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 403)

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

        # Retrieve username from db, duplicates not allowed
        with db.connect() as conn:
            # Execute query with .all() to select (hopefully) one row from the database
            name_check = conn.execute(text("SELECT username FROM users WHERE username = :a"), {"a": username}).all()
            
            # Check length of returned list, if item exists: set existing_user to inputted name; else: set to empty string
            if len(name_check) != 0:
                # Go into the object selecting the first tuple, then the first entry
                existing_user = name_check[0][0]
            else:
                existing_user = ""
        
        if username == "":
            flash("No username provided", error)
            # return redirect("/register")

        elif password == "":
            flash("No password provided", error)
            # return redirect("/register")

        elif password != passcheck:
            flash("Passwords don't match", error)
            # return redirect("/register")

        # Check for existing username
        elif existing_user == username:
            flash("Username is already taken", error)
            # return redirect("/register")

        else:
            # Hash password
            passhash = generate_password_hash(password)

            # Register user by adding to db
            with Session(db) as session:

                # Create new user
                newUser = user(
                    name = username,
                    password = passhash
                )

                ## Add user, then commit
                session.add_all(newUser)
                session.commit
                
            with db.connect() as conn:
                conn.execute(text("INSERT INTO users (username, password) VALUES (:a, :b)"), {"a": username, "b": passhash})
            # db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passhash)

            # Treat the new user as being logged in
            with db.connect() as conn:
                userid_table = conn.execute(text("SELECT id FROM users WHERE username = :a"), {"a": username})

            #userid_table = db.execute("SELECT id FROM users WHERE username = ?", username)
            print("test: " + str(userid_table))
            print(list(userid_table))
            session["user_id"] = userid_table[0]["id"]

            flash("You have been registered!")
            return redirect("/")
        
        # When checks are not passed, return to empty register-form
        return redirect("/register")

    else:
        return render_template("register.html")