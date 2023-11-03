from cs50 import SQL
import logging
from flask import Flask, current_app, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Set the desired log level


db = SQL("sqlite:///instagram.db")

app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = 'in05st05agr20am23'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(username):
    # Load the user from your SQLite database based on username
    query = "SELECT * FROM users WHERE username = :username"
    user_data = db.execute(query, username=username).fetchone()

    if user_data:
        user = User(user_data["id"], user_data["username"])
        return user

    return None  # Return None if the user is not found


@app.route("/")
def index():
    if session.get("username") is None:
        return redirect("/login")
    return render_template("home.html")


@app.route("/home")
@login_required
def home():
    if session.get("username") is None:
        return redirect("/login")
    return redirect('/')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        if password != confirmation:
            return render_template("password_error.html")
        
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return render_template("username_unavailable.html")
        
        password = generate_password_hash(password)
        
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)

        return redirect('/login')

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("user_error.html")

        session["username"] = request.form.get("username")

        return redirect("/")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session["username"] = None

    return redirect("/login")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1:
            return render_template("no_such_user.html")
        elif password != confirmation:
            return render_template("password_error.html")
        
        new_password = generate_password_hash(password)

        db.execute("UPDATE users SET password = (?) WHERE username = (?)", new_password, username)

        return redirect("/")

    return render_template("forgotten_password.html")