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


@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch('app.db.session.commit')
@patch('app.db.session.add')
@patch('app.models.user.User.set_password')
@patch('app.models.user.User.is_valid')
def test_create_account(
        mock_is_valid,
        mock_set_password,
        mock_add,
        mock_commit,
        mock_user_query,
        mock_token_decoder
):
    """Test authorized request returns success HTTP status code.
    """
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='vasuser',
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        is_admin=True,
        is_active=True
    )
    mock_token_decoder.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        'is_admin': True,
        'is_active': True
    }
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
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )

        assert response.status_code == 200


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(User, 'is_admin')
@patch.object(User, 'is_active')
@patch('app.db.session.commit')
@patch('app.db.session.add')
@patch('app.models.user.User.set_password')
@patch('app.models.user.User.is_valid')
def test_create_account_invalid_user(
        mock_is_valid,
        mock_set_password,
        mock_add,
        mock_commit,
        mock_is_active,
        mock_is_admin,
        mock_token_decoder,
        mock_user_query
):
    """Test authorized request returns success HTTP status code.
    """
    mock_is_active = True
    mock_is_admin = True
    mock_add = Mock()
    mock_commit = Mock()
    mock_is_valid.return_value = False
    mock_set_password.return_value = 'mock_password'
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='vasuser',
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        is_admin=False,
        is_active=True
    )
    mock_token_decoder.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        'is_admin': False,
        'is_active': True
    }
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
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )
        json_response_data = response.get_json()

        assert response.status_code == 403
        assert json_response_data['operationResult'] == 'FORBIDDEN: You do ' \
                                                        'not have the' \
                                                        ' permission to' \
                                                        ' perform operation.'


def test_create_account_token_missing():
    # Arrange
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json'
        }

        # Act
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
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )
        json_response_data = response.get_json()

        assert response.status_code == 403
        assert json_response_data['operationResult'] == 'TOKEN IS MISSING'


def test_create_account_invalid_token():
    # Arrange
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
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

        # Act
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )
        json_response_data = response.get_json()

        assert response.status_code == 403
        assert json_response_data['operationResult'] == 'INVALID TOKEN'


@patch('jwt.decode')
@patch('app.models.user.User.query')
def test_create_account_non_existent_user(
    mock_user_query,
    mock_token_decoder
):
    # Arrange
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
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
        mock_user_query.filter_by.return_value.first.return_value = None
        mock_token_decoder.return_value = {
            'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
            'is_admin': False,
            'is_active': True
        }

        # Act
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )
        json_response_data = response.get_json()

        assert response.status_code == 403
        assert json_response_data['operationResult'] == 'INVALID USER ' \
                                                        'CREDENTIALS'


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(User, 'is_admin')
@patch.object(User, 'is_active')
@patch('app.db.session.commit')
@patch('app.db.session.add')
@patch('app.models.user.User.set_password')
@patch('app.models.user.User.is_valid')
def test_create_account_already_existing(
    mock_is_valid,
    mock_set_password,
    mock_add,
    mock_commit,
    mock_is_active,
    mock_is_admin,
    mock_token_decoder,
    mock_user_query
):
    # Arrange
    mock_is_active = True
    mock_is_admin = True
    mock_add = Mock()
    mock_commit = Mock()
    mock_is_valid.return_value = False
    mock_set_password.return_value = 'mock_password'
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='vasuser',
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        is_admin=True,
        is_active=True
    )
    mock_token_decoder.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2',
        'is_admin': True,
        'is_active': True
    }
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }

        # Act
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
        response = app_test.post(
            '/inservices/api/v1.0/accounts/create',
            data=json.dumps(account_creator),
            content_type='application/json',
            headers=headers,
            follow_redirects=True
        )
        data = response.get_json()

        # Assert
        assert response.status_code == 409
        assert data['operationResult'] == 'NEW USER CREDENTIALS ALREADY TAKEN'
