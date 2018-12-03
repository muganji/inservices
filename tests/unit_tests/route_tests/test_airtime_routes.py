import json
from unittest.mock import patch

from app import app
from intelecom.intelecom import INConnection
from app.routes import airtime


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(airtime, 'debit_msisdn')
def test_debit_airtime(
        mock_debit_airtime,
        mock_login,
        mock_logout,
        mock_token,
        mock_user
):
    """
    Tests the debiting of airtime
    """
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
@patch.object(airtime, 'debit_msisdn')  
def test_failed_debit_airtime(
    mock_debit_airtime,
    mock_login,
    mock_logout,
    mock_token,
    mock_user
):
    """
    Tests the Failed debiting of airtime
    """
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

        assert response.status_code == 500

@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(airtime, 'credit_msisdn')
def test_credit_airtime(
    mock_credit_airtime,
    mock_login,
    mock_logout,
    mock_token,
    mock_user
):
    """
    Tests the crediting of airtime
    """
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
@patch.object(airtime, 'credit_msisdn')
def test_failed_credit_airtime(
    mock_credit_airtime,
    mock_login,
    mock_logout,
    mock_token,
    mock_user
):
    """
    Tests the Failed crediting of airtime
    """
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

        assert response.status_code == 500
