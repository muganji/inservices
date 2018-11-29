from base64 import b64encode
import json
import pdb
from unittest.mock import Mock, patch

from app import app
from app.models.user import User

import pytest


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
        encoded_credentials = b64encode(b"vasuser:1iyDjV")
        auth = encoded_credentials.decode('utf-8')
        response = app_test.get(
            '/inservices/api/v1.0/accounts/login',
            headers={
                "Authorization": f"Basic { auth }"})
        assert response.status_code == 200


@patch('app.models.user.User.query')
def test_login_user_not_found(mock_user_query):
    """Test authorized request returns success HTTP status code.
    """
    mock_user_query.filter_by.return_value.first.return_value = None

    with app.test_client() as app_test:
        encoded_credentials = b64encode(b"vasuser:1iyDjV")
        auth = encoded_credentials.decode('utf-8')
        response = app_test.get(
            '/inservices/api/v1.0/accounts/login',
            headers={
                "Authorization": f"Basic { auth }"})
        assert response.status_code == 403


@patch.object(User, 'check_password')
def test_login_invalid_password(mock_check_password):
    """Test authorized request returns success HTTP status code.
    """
    mock_check_password.return_value = False

    with app.test_client() as app_test:
        encoded_credentials = b64encode(b"vasuser:1iyDjV")
        auth = encoded_credentials.decode('utf-8')
        response = app_test.get(
            '/inservices/api/v1.0/accounts/login',
            headers={
                "Authorization": f"Basic { auth }"})
        assert response.status_code == 403


@patch('app.db.session.commit')
@patch('app.db.session.add')
@patch('app.models.user.User.set_password')
@patch('app.models.user.User.is_valid')
def test_create_account(
        mock_is_valid,
        mock_set_password,
        mock_add,
        mock_commit
):
    """Test authorized request returns success HTTP status code.
    """
    mock_add = Mock()
    mock_commit = Mock()
    mock_is_valid.return_value = True
    mock_set_password.return_value = 'mock_password'
    account_creator = {
        'Username': 'mock_user',
        'IsAdmin': True,
        'IsActive': True,
        'CanDebit': True,
        'CanCredit': True,
        'MmlUsername': 'mml',
        'MmlPassword': 'mml_pass',
        'UserType': 'ADMIN'
    }
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json'
        }
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )

        assert response.status_code == 200


@patch('app.db.session.commit')
@patch('app.db.session.add')
@patch('app.models.user.User.set_password')
@patch('app.models.user.User.is_valid')
def test_create_account_invalid_user(
        mock_is_valid,
        mock_set_password,
        mock_add,
        mock_commit
):
    """Test authorized request returns success HTTP status code.
    """
    mock_add = Mock()
    mock_commit = Mock()
    mock_is_valid.return_value = False
    mock_set_password.return_value = 'mock_password'
    account_creator = {
        'Username': 'mock_user',
        'IsAdmin': True,
        'IsActive': True,
        'CanDebit': True,
        'CanCredit': True,
        'MmlUsername': 'mml',
        'MmlPassword': 'mml_pass',
        'UserType': 'ADMIN'
    }
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json'
        }
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )

        assert response.status_code == 409
