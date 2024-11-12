from dotenv import load_dotenv
from flask import Flask, request
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
    SESSION_COOKIE_SECURE=True,  # Always use secure cookies in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',  # Required for cross-site cookies
    SESSION_COOKIE_DOMAIN=None,
)

# Get allowed origins from environment or use defaults
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://musaic-frontend-7a12a4566f21.herokuapp.com',
    'https://musaic-frontend.herokuapp.com',
    'https://musaic-backend-3d46a4f2ff11.herokuapp.com'
]

# Update CORS configuration
CORS(app, 
     origins=ALLOWED_ORIGINS,
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     expose_headers=["Set-Cookie", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "OPTIONS"])

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Register blueprints at the root level
app.register_blueprint(search_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)