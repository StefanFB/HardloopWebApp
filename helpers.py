from flask import redirect, render_template, request, session
from functools import wraps

# Be able to easily render an error message to the user
def error(message, code):
    return render_template("error.html", error=code, message=message), code

# Decorate routes to require login
# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function