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

# Test
@app.route("/")
@app.route("/get_books")
def get_books():
    return render_template("base.html", books=mongo.db.books.find())


# Deploying application on a server
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
