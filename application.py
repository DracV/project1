import os

from flask import Flask, render_template, request
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    headline = "My CS50W Book Review Website"
    return render_template ("index.html", headline=headline)

# users should be able to register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method =="GET":
        return "Please submit the form."
    else:
        name = request.form.get("name")
        return render_template ("register.html", name=name)

# users should be able to login
@app.route("/login")
def login():
    return "Login here"

# users should be able to logout
@app.route("/logout")
def logout():
    return "Logout here"

# users should be able to Search
@app.route("/search")
def search():
    return "Search here"

# users should be able to Book Page
@app.route("/books")
def books():
    return "Books here"





#   for login
#   <container id="main">
#       {% if logged in %}
#            <body> Show everything </body>
#       {% else %}  not logged in
#           <body> login form </body>
#       {% endif %}
#
