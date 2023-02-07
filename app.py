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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
@login_required
def add():
    return error("This page (add) has not yet been created", 404)

@app.route("/login")
def login():
    return error("This page (login) has not yet been created", 404)

@app.route("/overview")
@login_required
def overview():
    return error("This page (overview) has not yet been created", 404)

@app.route("/register")
def register():
    return error("This page (register) has not yet been created", 404)