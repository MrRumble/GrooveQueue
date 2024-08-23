from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api.guests.guest_routes import guest_bp
from api.bands.band_route import band_bp
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(guest_bp)
app.register_blueprint(band_bp)
# Initialize CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
