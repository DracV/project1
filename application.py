import os

from flask import Flask, render_template, request, session
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

@app.route("/register", methods=["GET","POST"])
def register():
    """Register for website"""

    headline = "Register Here"
    return render_template ("register.html", headline=headline)

# users should be able to register
@app.route("/newuser", methods=["POST"])
def newuser():
        """Add a new User"""

    #get user and pass and check if correct
        name = request.form.get('username')
        email = request.form.get("email")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE name = :name",{"name": name}).rowcount == 1:
            return render_template("/error.html", message="User name already taken")
        #if user != 'admin' or password != 'admin':
            #return render_template("register.html", message="Passwords wrong!")
        else:
            db.execute("INSERT INTO users (name, email, pass) VALUES (:name, :email, :pass)",
                {"name": name, "email": email, "pass": password})
            db.commit()
            return render_template("success.html", message="Registration successful!")

# users should be able to login TODO
@app.route("/login", methods=["GET","POST"])
def login():
    """Log In to website"""
    headline = "LogIn Here"
    # Get account information. - Name and Pass
    name = request.form.get("username")
    password = request.form.get("password")
    #session['username'] = name
    #session['password'] = password
    user = db.execute("SELECT * FROM users WHERE name =:name", {"name": name}).fetchall()
    if not user or not name or not password:
        return render_template('login.html', message="Missing Username or Password", logIn=False)
    else:
        #Test if submitted pass is legit
        if password == user[0][3]:
            return render_template("login.html", message="The password and username match")
        return render_template("login.html", message="Incorrect Username and/or password.")


# users should be able to logout TODO
@app.route("/logout")
def logout():
    return "Logout here"

# users should be able to Search TODO
@app.route("/search")
def search():
    return render_template ("search.html")

# users should be able to Book Page  TODO
@app.route("/books", methods=["GET", "POST"])
def books():
    if session.get("books") is None:
        session["books"] = []
    if request.method == "POST":
        book = request.form.get("book")
        session["books"].append(book)

    return render_template ("books.html", books=session["books"])






#@app.route('/login', methods=['POST', 'GET'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if valid_login(request.form['username'],
#                       request.form['password']):
#            return log_the_user_in(request.form['username'])
#        else:
#            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
#    return render_template('login.html', error=error)
