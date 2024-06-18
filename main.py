from environs import Env

from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
from string import ascii_letters, digits
from random import choice

env = Env()
env.read_env()

client = MongoClient(env.str("MONGODB_URI"))
database = client.url_shortener
BASE_URL = env.str("BASE_URL")

app = Flask(__name__)

def generate_short_url():
    """
    Generates a random 6-character string for the short URL using letters and digits.
    
    Returns:
        str: A random string of 6 characters.
    """
    characters = ascii_letters + digits
    short_url = "".join(choice(characters) for _ in range(6))
    return short_url

@app.route("/shorten", methods=["POST"])
def shorten_url():
    """
    Endpoint to shorten a long URL.
    
    Method:
        POST
        
    Request JSON:
        {
            "long_url": "http://example.com"
        }
        
    Returns:
        JSON response with the shortened URL.
        Example:
        {
            "short_url": "http://localhost:5000/ABC123"
        }
    """
    long_url = request.json["long_url"]
    short_url = generate_short_url()

    database.urls.insert_one({"long_url": long_url, "short_url": short_url})

    return jsonify({"short_url": BASE_URL + short_url}), 201

@app.route("/<short_url>")
def redirect_url(short_url):
    """
    Endpoint to redirect to the original long URL.
    
    Method:
        GET
        
    Path Parameter:
        short_url (str): The shortened URL path.
        
    Returns:
        A redirection to the original long URL if found.
        JSON response with an error message if not found.
        Example:
        {
            "error": "URL not found"
        }
    """
    url = database.urls.find_one({"short_url": short_url})

    if url is None:
        return jsonify({"error": "URL not found"}), 404

    return redirect(url["long_url"])

if __name__ == "__main__":
    app.run(debug=True)