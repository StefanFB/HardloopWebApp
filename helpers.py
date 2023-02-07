from flask import redirect, render_template, request, session

# Be able to easily render an error message to the user
def error(message, code):
    return render_template("error.html", error=code, message=message), code