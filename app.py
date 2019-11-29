import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Creating an application instance
app = Flask(__name__)

# Connecting application to database
app.config["MONGO_DBNAME"] = "book_reviews"
app.config["MONGO_URI"] = "mongodb+srv://Yaoma:pfc0a7aNQiF22Lek@cluster0-xbf5e.mongodb.net/book_reviews?retryWrites=true&w=majority"

# Creating an database instance
mongo = PyMongo(app)

# Fetching all books from database and rendering them to template
@app.route("/")
@app.route("/get_books")
def get_books():
    return render_template("get_books.html", books=mongo.db.books.find())

# Rendering form for adding new book to database
@app.route("/add_book")
def add_book():
    return render_template("add_book.html")

# Adding new book to database
@app.route("/insert_book", methods=["POST"])
def insert_book():
    # Getting list of books from database
    books = mongo.db.books
    # Converting data from form into dictionary and adding new book to database
    books.insert_one(request.form.to_dict())
    # Redirecting to home page
    return redirect(url_for("get_books"))


# Deploying application on a server
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
