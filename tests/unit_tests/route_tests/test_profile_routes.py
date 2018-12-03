
from unittest.mock import patch

from app import app

from intelecom.intelecom import INConnection

from app.routes import profile


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
#@patch.object(profile, 'get_msisdn_status')
def test_msisdn_status(
        #mock_account_info,
        mock_login,
        mock_logout,
        mock_token,
):
    """
    Testing the msisdn profile status.
    """
    msisdn = '712306172'
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjOTUxZmY2NC0wOTZiLTRkODYtYjRlNS03OGEwYzVlZTllNzUiLCJleHAiOjE1NDM1OTEzODF9.mF5FLJcZAQYOA-oZemxmIL6qcqd0qA3OrEdvRpijH_A'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/status/{msisdn}',
            headers=headers
        )

    assert response.status_code == 200


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
#@patch.object(profile, 'get_msisdn_status')
def test_msisdn_status_fails(
        #mock_account_info,
        mock_login,
        mock_logout,
        mock_token,
):
    """
    Testing the msisdn profile status.
    """
    msisdn = '712306173'
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjOTUxZmY2NC0wOTZiLTRkODYtYjRlNS03OGEwYzVlZTllNzUiLCJleHAiOjE1NDM1OTEzODF9.mF5FLJcZAQYOA-oZemxmIL6qcqd0qA3OrEdvRpijH_A'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/status/{msisdn}',
            headers=headers
        )

    assert response.status_code == 500


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
#@patch.object(profile, 'get_msisdn_balance')
def test_get_msisdn_balance(
        #mock_account_balance,
        mock_login,
        mock_logout,
        mock_token,
        mock_user
):
    """
    Testing the msisdn profile status and balance.
    """
    msisdn = '712306173'
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjOTUxZmY2NC0wOTZiLTRkODYtYjRlNS03OGEwYzVlZTllNzUiLCJleHAiOjE1NDM1OTEzODF9.mF5FLJcZAQYOA-oZemxmIL6qcqd0qA3OrEdvRpijH_A'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/balance/{msisdn}',
            headers=headers
        )

    assert response.status_code == 200


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
#@patch.object(profile, 'get_msisdn_balance')
def test_get_msisdn_balance_fails(
        #mock_account_balance,
        mock_login,
        mock_logout,
        mock_token,
        mock_user
):
    """
    Testing the msisdn profile status and balance.
    """
    msisdn = '712306173'
    with app.test_client() as test_app:
        headers = {
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjOTUxZmY2NC0wOTZiLTRkODYtYjRlNS03OGEwYzVlZTllNzUiLCJleHAiOjE1NDM1OTEzODF9.mF5FLJcZAQYOA-oZemxmIL6qcqd0qA3OrEdvRpijH_A'
        }
        response = test_app.get(
            f'/inservices/api/v1.0/profile/balance/{msisdn}',
            headers=headers
        )

    assert response.status_code == 500
