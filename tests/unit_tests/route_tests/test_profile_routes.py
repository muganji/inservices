import json
from unittest.mock import ANY, Mock, patch

from app import app
from app.models.user import User
from app.handlers.profile_handler import INRequestHandler


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'account_info')
def test_balance(
    mock_account_info,
    mock_init,
    mock_token,
    mock_user
):
    """
    Tests the debiting of airtime
    """
    mock_account_info.return_value = {
        'mobileNumber': '711187734',
        'balance': '5000',
        'subscriberProfile': '9',
        'status': 'ACTIVE'
    }
    mock_init.return_value = None
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    mock_user.return_value = User(
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    )
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
        response = app_test.get(
            '/inservices/api/v1.0/profile/balance/711187734',
            headers=headers
        )
        assert response.status_code == 200


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'account_info')
def test_profile(
    mock_account_info,
    mock_init,
    mock_token,
    mock_user
):
    """
    Tests the debiting of airtime
    """
    mock_account_info.return_value = {
        'mobileNumber': '711187734',
        'balance': '5000',
        'subscriberProfile': '9',
        'status': 'ACTIVE'
    }
    mock_init.return_value = None
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    mock_user.return_value = User(
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    )
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
        }
        response = app_test.get(
            '/inservices/api/v1.0/profile/711187734',
            headers=headers
        )
        assert response.status_code == 200
