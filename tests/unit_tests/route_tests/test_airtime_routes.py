import json
from unittest.mock import Mock, patch

from app import app
from app.models.user import User
from intelecom.intelecom import INConnection
from app.handlers.profile_handler import INRequestHandler
from app.decorators import token_required

@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INRequestHandler, 'debit_airtime')
def test_debit_airtime(mock_debit_airtime, mock_login, mock_logout, mock_token, mock_user):
    """
    Tests the debiting of airtime
    """
    mock_token.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    debitDetails = {'msisdn': '712306172', 'amount': 5000.0}
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
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 200


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INRequestHandler, 'debit_airtime')        
def test_failed_debit_airtime(mock_debit_airtime, mock_login, mock_logout, mock_token, mock_user):
    """
    Tests the Failed debiting of airtime
    """
    mock_token.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    debitDetails = {'msisdn': '712306172', 'amount': 700.0}
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
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers

        )

        assert response.status_code == 400

@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INRequestHandler, 'credit_airtime')
def test_credit_airtime(mock_credit_airtime, mock_login, mock_logout, mock_token, mock_user):
    """
    Tests the crediting of airtime
    """
    mock_token.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    creditDetails = {'msisdn': '712306172', 'amount': 5000.0}
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
            '/inservices/api/v1.0/airtime/credit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 200 


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INRequestHandler, 'credit_airtime')        
def test_failed_credit_airtime(mock_credit_airtime, mock_login, mock_logout, mock_token, mock_user):
    """
    Tests the Failed crediting of airtime
    """
    mock_token.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    creditDetails = {'msisdn': '712306172', 'amount': 700.0}
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
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers

        )

        assert response.status_code == 400