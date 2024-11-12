from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from music_ml.api.search import search_bp
from music_ml.api.generate_playlist import playlist_bp
from music_ml.api.auth import auth_bp
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.getenv('SECRET_KEY')

# Configure session
app.config.update(
    SESSION_COOKIE_SECURE=os.getenv('FLASK_ENV') == 'production',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_DOMAIN=None,
)

# Update CORS configuration
CORS(app, 
     origins=[
         'http://localhost:3000', 
         'http://127.0.0.1:3000',
         'https://musaic-frontend.herokuapp.com'  # Add your Heroku frontend URL
     ],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Set-Cookie"],
     methods=["GET", "POST", "OPTIONS"])

# Register blueprints at the root level
app.register_blueprint(search_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)