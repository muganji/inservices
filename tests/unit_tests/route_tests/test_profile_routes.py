<<<<<<< HEAD
from unittest.mock import Mock, patch

from app import app

from app.models.user import User

from app.handlers.profile_handler import INRequestHandler

from intelecom.intelecom import INQueryError





@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(INRequestHandler, 'account_info')
def test_msisdn_status(
        mock_account_info,
        mock_user_query,
        mock_token    
):
    """
    Testing the msisdn profile status.
    """
    msisdn = '712306172'
    transaction_id = Mock()
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='admin_julio',
        public_id='c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        is_admin=True,
        is_active=True
    )
    mock_token.return_value = {
        'public_id': 'public_id=c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        'is_admin': True,
        'is_active': True
    }
    mock_account_info.return_value = {
            'transactionId': transaction_id,
            'operationResult': 'Ok',
            'msisdn': msisdn,
            'status': 'Active',
            'message': 'Status query Successfull'
    }
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/status/{msisdn}',
            headers=headers
        )

        assert response.status_code == 200



@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'account_info',
        side_effect =INQueryError
    )
def test_msisdn_status_fails(
        mock_account_info,
        mock_user_query,
        mock_token
):
    """
    Testing the msisdn profile status fails.
    """
    msisdn = '712306172'
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='admin_julio',
        public_id='c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        is_admin=True,
        is_active=True
    )
    mock_token.return_value = {
        'public_id': 'public_id=c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        'is_admin': True,
        'is_active': True
    }
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/status/{msisdn}',
            headers=headers
        )

    assert response.status_code == 500


@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(INRequestHandler, 'account_info')
def test_get_msisdn_balance(
        mock_account_info,
        mock_user_query,
        mock_token
):
    """
    Testing the msisdn profile status and balance.
    """
    msisdn = '712306172'
    transaction_id = Mock()
    mock_account_info.return_value = {
            'transactionId': transaction_id,
            'operationResult': 'Ok',
            'msisdn': msisdn,
            'balance': 70000,
            'message': 'Balance query Successfull'
    }
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='admin_julio',
        public_id='c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        is_admin=True,
        is_active=True
    )
    mock_token.return_value = {
        'public_id': 'public_id=c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        'is_admin': True,
        'is_active': True
    }
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MDgwMDJ9.zqDjDXu7hXl59myppshkRy44Lg8jYDwy5V039zypxW8'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/balance/{msisdn}',
            headers=headers
        )

    assert response.status_code == 200


@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'account_info',
        side_effect =INQueryError
    )
def test_get_msisdn_balance_fails(
        mock_account_info,
        mock_user_query,
        mock_token
):
    """
    Testing the msisdn profile status and balance.
    """
    msisdn = '712306172'
    mock_user_query.filter_by.return_value.first.return_value = User(
        username='admin_julio',
        public_id='c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        is_admin=True,
        is_active=True
    )
    mock_token.return_value = {
        'public_id': 'public_id=c084bee1-d6a8-4bef-9a89-e34aad2d885d',
        'is_admin': True,
        'is_active': True
    }
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MDgwMDJ9.zqDjDXu7hXl59myppshkRy44Lg8jYDwy5V039zypxW8'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/balance/{msisdn}',
            headers=headers
        )

    assert response.status_code == 500
=======
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
>>>>>>> upstream/master
