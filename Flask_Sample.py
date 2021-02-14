# Import the Flask module that has been installed.
from flask import Flask,jsonify
from flask import request,escape
import sys

books = [
    {
        "id": 1,
        "title": "Harry Potter and the Goblet of Fire",
        "author": "J.K. Rowling",
        "isbn": "1512379298"
    },
    {
        "id": 2,
        "title": "Lord of the Flies",
        "author": "William Golding",
        "isbn": "0399501487"
    }
]
# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)

# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
def index():
    celsius = str(escape(request.args.get("celsius", "")))
    #celsius = request.args.get("celsius", "")
    return (
        """<form action="" method="get">
                <input type="text" name="celsius">
                <input type="submit" value="Convert">
            </form>"""
        + celsius
    )

@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
    return str(fahrenheit)

# Annotation that allows the function to be hit at the specific URL. Indicates a GET HTTP method.
@app.route("/library/v1.0/books", methods=["GET"])
# Function that will run when the endpoint is hit.
def get_books():
    # Returns a JSON of the books defined above. jsonify is a Flask function that serializes the object for us.
    return jsonify({"books": books})

# Annotation that allows the function to be hit at the specific URL. Indicates a GET HTTP method.
@app.route("/library/v1.0/books/<int:book_id>", methods=["GET"])
# Function that will run when the endpoint is hit.
def get_book(book_id):
    # Create an empty dictionary.
    result = {}

    # Loops through all the different books to find the one with the id that was entered.
    for book in books:
        # Checks if the id is the same as the parameter.
        if book["id"] == book_id:
            # Sets the result to the book and makes it a JSON.
            result = jsonify({"book": book})

    # Returns the book in JSON form or an empty dictionary. Should handle the error like 404, but will not cover here.
    return result

#HOST = sys.argv[1]
#PORT = int(sys.argv[2])
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)
