from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_talisman import Talisman
from music_ml.api.search import search_bp
from music_ml.api.generate_playlist import playlist_bp
from music_ml.api.auth import auth_bp
import logging
import os
import secrets

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.getenv('SECRET_KEY') or secrets.token_hex(32)
logger.debug(f"Using secret key: {'from env' if os.getenv('SECRET_KEY') else 'generated'}")

# Configure session
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

# Get allowed origins from environment or use defaults
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://musaic-frontend-7a12a4566f21.herokuapp.com',
    'https://musaic-frontend.herokuapp.com',
    'https://musaic-backend-3d46a4f2ff11.herokuapp.com'
]

# Initialize Talisman for HTTPS
talisman = Talisman(
    app,
    force_https=True,
    content_security_policy={
        'default-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", 'https:', 'data:'],
        'img-src': ["'self'", 'https:', 'data:'],
        'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'frame-ancestors': ["'none'"],
        'connect-src': ["'self'", "https://api.spotify.com"],
    },
    content_security_policy_nonce_in=['script-src'],
    feature_policy={
        'geolocation': "'none'",
        'microphone': "'none'",
        'camera': "'none'"
    }
)

# Update CORS configuration
CORS(app, 
     origins=ALLOWED_ORIGINS,
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

# Register blueprints at the root level
app.register_blueprint(search_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)