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

# Rendering for for editing record of selected book
@app.route("/edit_book/<book_id>")
def edit_book(book_id):
    # Find current book in database by unique id
    current_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("edit_book.html", book=current_book)

# Updating existing record of a book
@app.route("/update_book/<book_id>", methods=["POST"])
def update_book(book_id):
    # Getting list of books from database
    books = mongo.db.books
    # Finding current book in databse by unique id and updating it fields from form
    books.update({"_id": ObjectId(book_id)},
                 {
        "title": request.form.get("title"),
        "author": request.form.get("author")
    })
    # Redirecting to home page
    return redirect(url_for("get_books"))

# Remove selected book from database with all of it reviews
@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    # Find current book in database
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    # Remove all reviews of this book
    mongo.db.reviews.remove({"book_title": book["title"]})
    # Remove current from database
    mongo.db.books.remove({"_id": ObjectId(book_id)})
    return redirect(url_for("get_books"))

# Displaying reviews for selected book
@app.route("/get_reviews/<book_title>")
def get_reviews(book_title):
    # Getting all reviews for current book
    current_reviews = mongo.db.reviews.find({"book_title": book_title})
    return render_template("get_reviews.html", reviews=current_reviews, title=book_title)

# Displaying all reviews
@app.route("/get_all_reviews")
def get_all_reviews():
    return render_template("get_all_reviews.html", reviews=mongo.db.reviews.find())

# Creating new review for selected book
@app.route("/add_review/<book_title>")
def add_review(book_title):
    # Passing through book title for future database injection
    return render_template("add_review.html", title=book_title)

# Injecting database with new review
@app.route("/insert_review/<book_title>", methods=["POST"])
def insert_review(book_title):
    # Getting list of reviews
    reviews = mongo.db.reviews
    # Creating new review with selected book title for future sorting
    new_review = {"book_title": book_title}
    # Adding rest of fields from form
    new_review.update(request.form.to_dict())
    # Adding new review to database
    reviews.insert_one(new_review)
    # Redirecting back to current book reviews
    return redirect(url_for("get_reviews", book_title=book_title))


# Deploying application on a server
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
