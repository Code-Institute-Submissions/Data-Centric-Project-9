import os
from flask import Flask

# Creating and application instance.
app = Flask(__name__)

# Test
@app.route("/")
def test():
    return "Test Message"


# Deploying application on a server
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
