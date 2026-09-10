from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from chatbot import find_best_answer


# =========================================================
# Flask Application
# =========================================================

app = Flask(__name__)

# Secret key for secure session management
# For a college/local project this is fine.
# In a real production application, keep this in an
# environment variable instead of hardcoding it.
app.secret_key = "python-qa-chatbot-secret-key"


# =========================================================
# Temporary User Storage
# =========================================================
#
# Users are stored in memory for now.
#
# Structure:
#
# users = {
#     "username": {
#         "username": "...",
#         "email": "...",
#         "password": "hashed password"
#     }
# }
#
# IMPORTANT:
# Since this is in-memory storage, registered users will be
# cleared whenever Flask is restarted.
#
# We can add SQLite/database persistence later if needed.
# =========================================================

users = {}


# =========================================================
# Helper Functions
# =========================================================

def find_user_by_login_id(login_id):
    """
    Find a user using either:
    - Username
    - Email ID

    Username and email comparison are case-insensitive.
    """

    login_id = login_id.strip().lower()

    if not login_id:
        return None

    # Check username
    for user in users.values():

        if user["username"].lower() == login_id:
            return user

    # Check email
    for user in users.values():

        if user["email"].lower() == login_id:
            return user

    return None


def username_exists(username):
    """
    Check whether username already exists.
    """

    username = username.strip().lower()

    for user in users.values():

        if user["username"].lower() == username:
            return True

    return False


def email_exists(email):
    """
    Check whether email already exists.
    """

    email = email.strip().lower()

    for user in users.values():

        if user["email"].lower() == email:
            return True

    return False


# =========================================================
# Home / Chatbot Page
# =========================================================

@app.route("/")
def home():

    # User must login before accessing chatbot

    if "username" not in session:
        return render_template("login.html")

    return render_template("index.html")


# =========================================================
# Register Page
# =========================================================

@app.route("/register", methods=["GET"])
def register_page():

    # If already logged in, go directly to chatbot

    if "username" in session:
        return render_template("index.html")

    return render_template("register.html")


# =========================================================
# Register User
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    # Support JSON request
    data = request.get_json(silent=True)

    if data is None:
        data = request.form

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")


    # -----------------------------------------------------
    # Empty field validation
    # -----------------------------------------------------

    if not username:
        return jsonify({
            "success": False,
            "message": "Please enter a username."
        }), 400


    if not email:
        return jsonify({
            "success": False,
            "message": "Please enter your email ID."
        }), 400


    if not password:
        return jsonify({
            "success": False,
            "message": "Please enter a password."
        }), 400


    if not confirm_password:
        return jsonify({
            "success": False,
            "message": "Please confirm your password."
        }), 400


    # -----------------------------------------------------
    # Username validation
    # -----------------------------------------------------

    if len(username) < 3:
        return jsonify({
            "success": False,
            "message": "Username must contain at least 3 characters."
        }), 400


    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    if "@" not in email or "." not in email:

        return jsonify({
            "success": False,
            "message": "Please enter a valid email ID."
        }), 400


    # -----------------------------------------------------
    # Password validation
    # -----------------------------------------------------

    if len(password) < 8:

        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters."
        }), 400


    # -----------------------------------------------------
    # Confirm password
    # -----------------------------------------------------

    if password != confirm_password:

        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400


    # -----------------------------------------------------
    # Duplicate username
    # -----------------------------------------------------

    if username_exists(username):

        return jsonify({
            "success": False,
            "message": "Username already exists. Please choose another username."
        }), 409


    # -----------------------------------------------------
    # Duplicate email
    # -----------------------------------------------------

    if email_exists(email):

        return jsonify({
            "success": False,
            "message": "Email ID already registered. Please use another email."
        }), 409


    # -----------------------------------------------------
    # Hash password
    # -----------------------------------------------------

    hashed_password = generate_password_hash(password)


    # -----------------------------------------------------
    # Create user
    # -----------------------------------------------------

    users[username] = {

        "username": username,

        "email": email,

        "password": hashed_password
    }


    # -----------------------------------------------------
    # Registration successful
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "message": "Account created successfully."
    }), 201


# =========================================================
# Login Page
# =========================================================

@app.route("/login", methods=["GET"])
def login_page():

    if "username" in session:
        return render_template("index.html")

    return render_template("login.html")


# =========================================================
# Login User
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    # Support JSON and normal form requests

    data = request.get_json(silent=True)

    if data is None:
        data = request.form


    # Login frontend sends:
    #
    # login_id
    # password

    login_id = data.get("login_id", "").strip()
    password = data.get("password", "")


    # -----------------------------------------------------
    # Empty login ID
    # -----------------------------------------------------

    if not login_id:

        return jsonify({
            "success": False,
            "message": "Please enter your username or email ID."
        }), 400


    # -----------------------------------------------------
    # Empty password
    # -----------------------------------------------------

    if not password:

        return jsonify({
            "success": False,
            "message": "Please enter your password."
        }), 400


    # -----------------------------------------------------
    # Find user
    # -----------------------------------------------------

    user = find_user_by_login_id(login_id)


    if user is None:

        return jsonify({
            "success": False,
            "message": "Invalid username/email or password."
        }), 401


    # -----------------------------------------------------
    # Verify password
    # -----------------------------------------------------

    if not check_password_hash(
        user["password"],
        password
    ):

        return jsonify({
            "success": False,
            "message": "Invalid username/email or password."
        }), 401


    # -----------------------------------------------------
    # Create login session
    # -----------------------------------------------------

    session["username"] = user["username"]

    session["email"] = user["email"]


    # -----------------------------------------------------
    # Login successful
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "message": "Login successful.",

        "username": user["username"],

        "email": user["email"]
    }), 200


# =========================================================
# Check Login Status
# =========================================================

@app.route("/check-login", methods=["GET"])
def check_login():

    if "username" not in session:

        return jsonify({

            "logged_in": False

        }), 401


    return jsonify({

        "logged_in": True,

        "username": session["username"],

        "email": session.get("email", "")
    })


# =========================================================
# Logout
# =========================================================

@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    return jsonify({

        "success": True,

        "message": "Logged out successfully."
    })


# =========================================================
# Ask Python Question
# =========================================================

@app.route("/ask", methods=["POST"])
def ask():

    # -----------------------------------------------------
    # Login protection
    # -----------------------------------------------------

    if "username" not in session:

        return jsonify({

            "success": False,

            "answer":
                "Please login before using the Python Q&A Chatbot.",

            "logged_in": False

        }), 401


    # -----------------------------------------------------
    # Read request
    # -----------------------------------------------------

    data = request.get_json(silent=True)


    if data is None:

        return jsonify({

            "success": False,

            "answer":
                "Invalid request."

        }), 400


    question = data.get(
        "question",
        ""
    ).strip()


    # -----------------------------------------------------
    # Empty question
    # -----------------------------------------------------

    if not question:

        return jsonify({

            "success": False,

            "answer":
                "Please enter a question."

        }), 400


    # -----------------------------------------------------
    # Find answer
    # -----------------------------------------------------

    answer = find_best_answer(question)


    # -----------------------------------------------------
    # Return answer
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "answer": answer
    })


# =========================================================
# Application Start
# =========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("              PYTHON Q&A CHATBOT")

    print("=" * 60)

    print("Authentication: Enabled")

    print("Login: Username or Email ID")

    print("Password: Securely Hashed")

    print("Python Q&A: Enabled")

    print("Server: http://127.0.0.1:5000")

    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )