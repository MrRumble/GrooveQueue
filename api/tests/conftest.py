import pytest, sys, random, py, pytest, os
from xprocess import ProcessStarter
from api.common.db import DatabaseConnection
from api.main import app
from werkzeug.security import generate_password_hash

# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.
@pytest.fixture
def db_connection():
    conn = DatabaseConnection(test_mode=True)
    conn.connect()
    return conn

# This fixture starts the test server and makes it available to the tests.
# You don't need to understand it in detail.
@pytest.fixture
def test_web_address(xprocess):
    python_executable = sys.executable
    app_file = py.path.local(__file__).dirpath("../app.py")
    port = str(random.randint(4000, 4999))
    class Starter(ProcessStarter):
        env = {"PORT": port, "APP_ENV": "test", **os.environ}
        pattern = "Debugger PIN"
        args = [python_executable, app_file]

    xprocess.ensure("flask_test_server", Starter)

    yield f"localhost:{port}"

    xprocess.getinfo("flask_test_server").terminate()

@pytest.fixture
def web_client():
    app.config['TESTING'] = True # This gets us better errors
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def auth_headers(db_connection):
    # Prepare test data
    test_band_email = "white_noise@example.com"
    test_band_password = "bandpass123"

    # Create a test band in the database with hashed password
    connection = db_connection
    hashed_password = generate_password_hash(test_band_password)

    # Insert the test band into the database (adjust the query as per your DB schema)
    connection.execute("""
        INSERT INTO bands (band_name, band_email, password) 
        VALUES (%s, %s, %s)
    """, ("White Noise", test_band_email, hashed_password))

    with app.test_client() as client:
        # Log in to get the token
        response = client.post('/bands/login', json={
            'band_email': test_band_email,
            'password': test_band_password
        })

        # Assert the response status code and extract the token
        assert response.status_code == 200, "Login failed: " + response.get_json().get("error", "")
        response_json = response.get_json()
        token = response_json['access_token']

        return {
            "Authorization": f"Bearer {token}"
        }