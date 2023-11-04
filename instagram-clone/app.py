from cs50 import SQL
import logging
from flask import Flask, current_app, flash, redirect, render_template, request, session, url_for, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
from user_module import User

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Set the desired log level


db = SQL("sqlite:///instagram.db")

app.config['SECRET_KEY'] = 'in05st05agr20am23'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    # Convert the user_id to an integer (assuming it's an integer) if necessary
    user_id = int(user_id)

    # Load the user from your SQLite database based on user_id
    user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    if user_data:
        user_data = user_data[0]
        user = User(user_data["id"], user_data["username"])
        return user
    
    print("User not found for user_id:", user_id)
    return None  # Return None if the user is not found


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template("home.html")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        if password != confirmation:
            return render_template("password_error.html")
        
        existing_user = db.execute("SELECT * FROM users WHERE username = (?)", username)
        if existing_user:
            return render_template("username_unavailable.html")
        
        password = generate_password_hash(password)
        
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)

        flash("Registered!")

        return redirect('/login')

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve the user from the database based on the provided username
        user_data = db.execute("SELECT * FROM users WHERE username = (?)", username)
        if user_data and check_password_hash(user_data[0]["password"], password):
            # Create a User object based on the user data
            user = User(user_data[0]["id"], user_data[0]["username"])
            session["username"] = user_data[0]["username"]

            # Authenticate the user using Flask-Login
            login_user(user)

            print("User authenticated:", username) 

            # Redirect to the desired page after successful login (e.g., home)
            return redirect("/home")
        else:
            print("User authentication failed:", username)
            return render_template("user_error.html")
    
    return render_template("login.html", messages=get_flashed_messages())


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        rows = db.execute("SELECT * FROM users WHERE username = (?)", username)
        if len(rows) != 1:
            return render_template("no_such_user.html")
        if password != confirmation:
            return render_template("password_error.html")
        
        new_password = generate_password_hash(password)

        db.execute("UPDATE users SET password = (?) WHERE username = (?)", new_password, username)

        flash("Password Changed!")

        return redirect("/")

    return render_template("forgotten_password.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/messages")
@login_required
def messages():
    return render_template("messages.html")