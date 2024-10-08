from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from api.guests.guest_routes import guest_bp
from api.bands.band_route import band_bp
from api.events.events_routes import event_bp
from api.requests.request_routes import request_bp

import os

# Load environment variables python -m api.main

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Configuration for JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Register the blueprint
app.register_blueprint(guest_bp)
app.register_blueprint(band_bp)
app.register_blueprint(event_bp)
app.register_blueprint(request_bp)

# Initialize CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
