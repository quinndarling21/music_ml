from flask import Flask
from api.search import search_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(search_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)