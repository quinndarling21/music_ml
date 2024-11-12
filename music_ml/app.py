from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import logging
import os
import secrets

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
if os.getenv('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev-secret-key'),
    SESSION_TYPE='sqlalchemy',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    SESSION_COOKIE_NAME='spotify_auth_session',
    SESSION_COOKIE_SECURE=False if os.getenv('FLASK_ENV') == 'development' else True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax' if os.getenv('FLASK_ENV') == 'development' else 'None',
    SESSION_COOKIE_DOMAIN='127.0.0.1' if os.getenv('FLASK_ENV') == 'development' else None
)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

# Initialize Flask-Session
Session(app)

# Create tables
with app.app_context():
    db.create_all()

# Define allowed origins
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
     expose_headers=["Set-Cookie"],
     methods=["GET", "POST", "OPTIONS"])

@app.after_request
def after_request(response):
    if os.getenv('FLASK_ENV') == 'development':
        response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
    else:
        response.headers.add('Access-Control-Allow-Origin', 'https://musaic-frontend-7a12a4566f21.herokuapp.com')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Import and register blueprints
from music_ml.api.search import search_bp
from music_ml.api.generate_playlist import playlist_bp
from music_ml.api.auth import auth_bp

app.register_blueprint(search_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)