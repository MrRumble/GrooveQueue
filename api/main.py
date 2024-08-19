import os
from flask import Flask
import psycopg
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)


# Initialize CORS
CORS(app)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
