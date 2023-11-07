from cs50 import SQL
from flask_socketio import SocketIO
import logging
from flask import Flask, current_app, flash, redirect, render_template, request, session, url_for, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
from user_module import User
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.expanduser('~/images')
app.logger.setLevel(logging.DEBUG)  # Set the desired log levels


db = SQL("sqlite:///instagram.db")
socketio = SocketIO(app)

db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

app.config['SECRET_KEY'] = 'in05st05agr20am23'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# @socketio.on('join_chat')
# def join_chat(data):
#     sender_id = data['sender_id']
#     receiver_id = data['receiver_id']
#     chat_room = f"{sender_id}_{receiver_id}"

#     socketio.join_room(chat_room)

# @socketio.on('send_message')
# def handle_message(data):
#     sender_id = data['sender_id']
#     receiver_id = data['receiver_id']
#     content = data['content']
#     chat_room = f"{sender_id}_{receiver_id}"

#     db.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)", sender_id, receiver_id, content)
    
#     socketio.emit('message', data, room=chat_room)


@login_manager.user_loader
def load_user(user_id):
    # Convert the user_id to an integer (assuming it's an integer) if necessary
    user_id = int(user_id)

    # Load the user from your SQLite database based on user_id
    user_data = db.execute("SELECT * FROM users WHERE id = (?)", user_id)

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

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        user_id = db.execute("SELECT id FROM users WHERE username = (?)", session["username"])
        if user_id: 
            user_id = int(user_id[0]["id"])
        content = request.form.get('content')
        image_path = request.form.get("image")
        
        if user_id:
            db.execute("INSERT INTO post (user_id, content, image_path) VALUES (?, ?, ?)", user_id, content, image_path)
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route("/home")
@login_required
def home():
    posts = db.execute("SELECT * FROM post")
    posts_info = []
    for post in posts:
        id = post["id"]
        user_id = post["user_id"]
        content = post["content"]
        image_path = post["image_path"]
        username = db.execute("SELECT username FROM users WHERE id = (?)", user_id)
        if username:
            username = username[0]["username"]

        if username:    
            post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path, "username": username}
        else:
            post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path}
        
        posts_info.append(post_info)

    
    return render_template("home.html", posts=posts_info)

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
    posts = db.execute("SELECT * FROM post")
    posts_info = []
    for post in posts:
        id = post["id"]
        user_id = post["user_id"]
        content = post["content"]
        image_path = post["image_path"]
        username = db.execute("SELECT username FROM users WHERE id = (?)", user_id)
        if username:
            username = username[0]["username"]

        if username:    
            post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path, "username": username}
        else:
            post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path}
        
        posts_info.append(post_info)

    return render_template("profile.html", posts = posts_info)

@app.route("/messages")
@login_required
def messages():
    return render_template("messages.html")

@app.route("/delete_post", methods=["GET", "POST"])
@login_required
def delete_post():
    post_id = int(request.form.get('post_id'))
    db.execute("DELETE FROM post WHERE id = (?)", post_id)
    return redirect(url_for('home'))


@app.route("/user/<username>")
def user_profile(username):
    user_info = db.execute("SELECT * FROM users WHERE username = ?", username)
    user_id = db.execute("SELECT id FROM users WHERE username = (?)", username)
    user_id = int(user_id[0]["id"])
    users = db.execute("SELECT * FROM users WHERE id = (?)", user_id)

    if user_info:
        # Render the user profile template and pass the user-specific data
        posts = db.execute("SELECT * FROM post")
        posts_info = []
        for post in posts:
            id = post["id"]
            user_id = post["user_id"]
            content = post["content"]
            image_path = post["image_path"]
            username = db.execute("SELECT username FROM users WHERE id = (?)", user_id)
            if username:
                username = username[0]["username"]

            if username:    
                post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path, "username": username}
            else:
                post_info = {"id": id, "user_id": user_id, "content": content, "image_path": image_path}
            
            posts_info.append(post_info)

        users_info = []
        for user in users:
            id = user["id"]
            user_info = {"id": id}
            users_info.append(user_info)

        return render_template("user_profile.html", posts=posts_info, users=users_info)
    else:
        # Handle the case where the username doesn't exist
        return render_template("user_not_found.html")
