import json
from unittest.mock import Mock, patch

from app import app
from app.handlers.profile_handler import INRequestHandler
from app.models.user import User
from intelecom.intelecom import INQueryError


@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'debit_airtime'
    )
def test_debit_airtime(
        mock_debit_airtime,
        mock_user_query,
        mock_token
):
    """
    Test for debiting of airtime
    """
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
    debitDetails = {"msisdn": "712306172", "amount": "700.0"}
    transaction_id = Mock()

    mock_debit_airtime.return_value = {
            'transactionId': transaction_id,
            'operationResult': 'Ok',
            'msisdn': 712306172,
            'amount': 1000,
            'message': 'Debit query successfull'
        }
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 200


@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'debit_airtime',
        side_effect =INQueryError
    )
def test_failed_debit_airtime(
        mock_account_info,
        mock_user_query,
        mock_token
):
    """
    Test for Failed debiting of airtime
    """
    debitDetails = {"msisdn": "712306172", "amount": "700.0"}
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
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
            
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers

        )

        assert response.status_code == 500

@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'credit_airtime'
    )
def test_credit_airtime(
        mock_credit_airtime,
        mock_user_query,
        mock_token
):
    """
    Test for crediting of airtime
    """
    creditDetails = {"msisdn": "712306172", "amount": "700.0"}
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
    transaction_id = Mock()
    mock_credit_airtime.return_value = {
            'transactionId': transaction_id,
            'operationResult': 'Ok',
            'msisdn': 712306172,
            'amount': 1000,
            'message': 'Credit query Successful'
        }
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'    
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/credit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 200 

@patch('jwt.decode')
@patch('app.models.user.User.query')
@patch.object(
        INRequestHandler,
        'credit_airtime',
        side_effect =INQueryError
    )
def test_failed_credit_airtime(
        mock_account_info,
        mock_user_query,
        mock_token
):
    """
    Test for Failed crediting of airtime
    """
    creditDetails = {"msisdn": "712306172", "amount": "700.0"}
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
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
            
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/credit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers

        )

        assert response.status_code == 500

