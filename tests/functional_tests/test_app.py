from text_labeller import create_app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Register as a user or login" in response.data
        assert b"TextLabeller is a free platform for labelling" in response.data
        assert b"Welcome to the a Flask app!" not in response.data

def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200
        assert b"Log In" in response.data
        assert b"Email" in response.data

def test_register_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/register')
        assert response.status_code == 200
        assert b"Password" in response.data
        assert b"Email" in response.data