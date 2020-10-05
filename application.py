import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///covid.db")

# Guest page
@app.route("/")
def guest():
    # covid data global
    
    info = lookup('Global')
    
    return render_template("guest.html", info=info)

# Main page after login
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'GET':
    
        info = lookup('Global')
        
        return render_template("index.html", data=info['Global'])
    else:
        # Searches covid data by countries
        country = request.form.get("country")
        info = lookup("Country")
        
        # Looks for actual country which exists, if exists returns
        for data in info['Country']:
            if data['Country'] == country:
                return render_template("index.html", data=data)
            
        # If country not exist    
        flash("No Data!")
        return redirect("/index")
        

        
        
# login
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

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        users = db.execute("SELECT * FROM users")

        if username in users:
            return apology("username already exists")
        elif username == '':
            return apology("must provide a username")

        if password == '':
            return apology("must provide a password")

        elif password != confirmation:
            return apology("password doesn't match")

        # Keeps password as hash value
        hashpassword = generate_password_hash(password)

        new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=hashpassword)

        # unique username constraint violated?
        if not new_user:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user

        # Display a flash message
        flash("Registered!")

        return redirect("/index")
