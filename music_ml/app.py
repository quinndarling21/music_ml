from flask import Flask
from dotenv import load_dotenv
import os

from flask_cors import CORS  # Import the CORS library
from api.search import search_bp
from api.generate_playlist import playlist_bp

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Enable CORS for the frontend origin

# Register blueprints
app.register_blueprint(search_bp)
app.register_blueprint(playlist_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)