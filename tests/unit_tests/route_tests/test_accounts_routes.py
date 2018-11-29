from base64 import b64encode
from app import app


def test_login_forbidden_no_authorization():
    """Test unauthorized request is forbidden.
    """
    with app.test_client() as app_test:
        response = app_test.get('/inservices/api/v1.0/accounts/login')
        assert response.status_code == 403


def test_login_authorized():
    """Test authorized request returns success HTTP status code.
    """
    with app.test_client() as app_test:
        encoded_credentials = b64encode(b"vasuser:vasuser")
        auth = encoded_credentials.decode('utf-8')
        response = app_test.get(
            '/inservices/api/v1.0/accounts/login',
            headers={
                "Authorization": f"Basic { auth }"})
        print(response.status_code, response.data)
        assert response.status_code == 200


def test_create_account():
    """Test authorized request returns success HTTP status code.
    """
    with app.test_client() as app_test:
        response = app_test.get('/inservices/api/v1.0/accounts/create')
        assert response.status_code == 200
