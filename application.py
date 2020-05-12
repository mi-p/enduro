import os
import requests

from flask import Flask, session, request, render_template, redirect, url_for, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug import security
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
json = FlaskJSON(app)
app.config['JSON_ADD_STATUS'] = False
app.config['JSON_SORT_KEYS'] = False


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

if not (engine.dialect.has_table(engine, "users") and engine.dialect.has_table(engine, "books") and engine.dialect.has_table(engine, "reviews")):
    create_tables()

@app.route("/")
def index():
    #cheks if user is logged in and shows search or login page
    if session.get('login')==1:
        session['books'] = "Brak"
        return render_template("index.html", message="")
    else:
        if request.args.get("message") != None:
            message = request.args.get("message")
        else:
            message = "Hello, please log in or register"
        return render_template("login.html", message=message)

@app.route("/login", methods=["POST"])
def login_check():
    usercred = db.execute("SELECT * FROM users WHERE username = :name", {"name":request.form.get("name")}).fetchone()
    db.remove()
    if usercred == None:
        return redirect(url_for('index', message="No such username, please try again or register"))
    if security.check_password_hash(str(usercred[2]), request.form.get("password")):
        session['user']=request.form.get('name')
        session['user_id']=usercred[0]
        session['login']=1
    else:
        return redirect(url_for('index', message="Invalid password"))
    return redirect(url_for('index'))

@app.route("/register", methods=["POST"])
def register_post():
    #add user to database and set login status to 1
    if request.form.get('name') != None:
        session['user']=request.form.get('name')
        db.execute("INSERT INTO users (username, passwordh) VALUES (:user, :pwdh);", { "user":request.form.get('name'), "pwdh":security.generate_password_hash(request.form.get('password'))})
        db.commit()
        session['user_id'] = db.execute("SELECT id FROM users WHERE username = :name", {"name":request.form.get("name")}).fetchone()[0]
        session['login']=1
    return redirect('/')

@app.route("/logout", methods=["POST"])
def logout():
    session['login']=0
    return redirect('/')

@app.route("/books", methods=["POST"])
def search_result():
    if session['books'] != "Brak":
        return render_template("search_result.html", books = session['books'])
    #prepare database query and use SESSION to remember user search
    author = "%" + request.form.get("author") + "%"
    title = "%" + request.form.get("title") + "%"
    isbn = "%" + request.form.get("number") + "%"
    a = ""
    t = ""
    i = ""

    if author != "%%":
        a= "author LIKE :author"
        if title != "%%" or isbn != "%%":
            a = a + ", "
    if title != "%%":
        t = "title LIKE :title"
        if isbn != "%%":
            t = t + ", "
    if isbn != "%%":
        i = "isbn LIKE :isbn"

    books = "SELECT * FROM books WHERE (" + a + t + i +")"
    books = db.execute(books, {"author":author, "title":title, "isbn":isbn }).fetchall()
    session['books'] = books
    return render_template("search_result.html", books = books)

@app.route("/book/<isbn>", methods=["POST", "GET"])#/{isbn}")
def book(isbn):
    b = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    session['book'] = b
    b_r = db.execute("SELECT * FROM reviews JOIN users ON user_id=users.id WHERE book_isbn=:isbn ", {"isbn":isbn}).fetchall()
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "v24K5qLwzmLXpmtsZH49Sw", "isbns":isbn}).json()["books"][0]
    already = db.execute("SELECT * FROM reviews WHERE (book_isbn=:isbn AND user_id=:user_id)", {"isbn":isbn, "user_id":session['user_id']}).fetchone()
    return render_template("book.html", book=b, reviews=b_r, gr = goodreads, already=already)

@app.route("/review/<isbn>", methods=['POST'])
def add_review(isbn):
    #Add review

    rate = db.execute("SELECT review_count, average_score FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if rate[0] == None:
        rate = [0,0]
    new_score = (rate[1]*rate[0]+int(request.form.get("score")))/(rate[0]+1)
    db.execute("UPDATE books SET review_count = :review_count + 1, average_score=:new_score WHERE isbn=:isbn", {"new_score":new_score, "isbn":isbn, "review_count":rate[0]})
    #added review_count substitution because if it was empty then SET review_conut = review_count + 1 didn't work
    db.execute("INSERT INTO reviews (user_id, book_isbn, rating, review) VALUES (:user_id, :isbn, :rating, :review)", {"user_id":session.get("user_id"), "isbn":isbn, "rating":request.form.get("score"), "review":request.form.get("review")})
    db.commit()
    return redirect(url_for("book", isbn=isbn))

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if book == None:
        return abort(404, description="Are you sure someone wrote that book? ISBN not found")
    return json_response(title=book[1], \
        author=book[2], \
        year = book[3], \
        isbn = book[0], \
        review_count = book[4], \
        average_score=book[5])


def create_tables():
  # Create database tables for users, books and reviews
  db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, passwordh VARCHAR NOT NULL);")
  db.execute("CREATE TABLE books (\
    isbn VARCHAR PRIMARY KEY, \
    title VARCHAR NOT NULL, \
    author VARCHAR NOT NULL, \
    year INTEGER, \
    review_count INTEGER, \
    average_score REAL \
    ); ")
  db.execute("CREATE TABLE reviews (\
    id SERIAL PRIMARY KEY, \
    book_isbn VARCHAR REFERENCES books, \
    user_id INTEGER REFERENCES users, \
    rating INTEGER, \
    review VARCHAR \
    ); ")
  db.commit()
