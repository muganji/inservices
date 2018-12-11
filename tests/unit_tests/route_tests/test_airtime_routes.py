import json
from unittest.mock import Mock, patch

from app import app
from app.handlers.profile_handler import INRequestHandler
from app.models.user import User
from intelecom.intelecom import INQueryError


<<<<<<< HEAD
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
=======

@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'debit_airtime')
def test_debit_airtime(
    mock_debit_airtime,
    mock_init,
    mock_token,
    mock_user
>>>>>>> upstream/master
):
    """
    Test for debiting of airtime
    """
<<<<<<< HEAD
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
=======
    mock_debit_airtime.return_value = True
    mock_init.return_value = None
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    mock_user.return_value = User(
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    )
    debitDetails = {'msisdn': '712306172', 'amount': 5000.0}
>>>>>>> upstream/master
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
<<<<<<< HEAD
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
=======
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
>>>>>>> upstream/master
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers
        )
        assert response.status_code == 200


@patch('jwt.decode')
<<<<<<< HEAD
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
=======
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'debit_airtime')
def test_failed_debit_airtime(
    mock_debit_airtime,
    mock_inrequesthandler_init,
    mock_token,
    mock_user
>>>>>>> upstream/master
):
    """
    Test for Failed debiting of airtime
    """
<<<<<<< HEAD
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
=======
    mock_inrequesthandler_init.return_value = None
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    debitDetails = {'msisdn': '712306172', 'amount': 700.0}
    mock_debit_airtime.return_value = False
>>>>>>> upstream/master
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
<<<<<<< HEAD
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'    
=======
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'
>>>>>>> upstream/master
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/debit',
            data=json.dumps(debitDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 500

<<<<<<< HEAD
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
=======
        assert response.status_code == 400


@patch('app.models.user.User.query')
@patch('jwt.decode')
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'credit_airtime')
def test_credit_airtime(
    mock_credit_airtime,
    mock_inrequesthandler_init,
    mock_token,
    mock_user
>>>>>>> upstream/master
):
    """
    Test for crediting of airtime
    """
<<<<<<< HEAD
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
=======
    mock_user.return_value = User(
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    )
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    mock_credit_airtime.return_value = True
    mock_inrequesthandler_init.return_value = None
    creditDetails = {'msisdn': '712306172', 'amount': 5000.0}
>>>>>>> upstream/master
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
<<<<<<< HEAD
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'    
=======
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'

>>>>>>> upstream/master
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/credit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers
        )
        assert response.status_code == 200

@patch('jwt.decode')
<<<<<<< HEAD
@patch('app.models.user.User.query')
@patch.object(INRequestHandler, 'credit_airtime', side_effect =INQueryError)
def test_failed_credit_airtime(
        mock_account_info,
        mock_user_query,
        mock_token
=======
@patch.object(INRequestHandler, '__init__')
@patch.object(INRequestHandler, 'credit_airtime')       
def test_failed_credit_airtime(
    mock_credit_airtime,
    mock_inrequesthandler_init,
    mock_token,
    mock_user
>>>>>>> upstream/master
):
    """
    Test for Failed crediting of airtime
    """
<<<<<<< HEAD
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
=======
    mock_user.return_value = User(
        public_id='f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    )
    mock_inrequesthandler_init.return_value = None
    mock_token.return_value = {
        'public_id': 'f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    mock_credit_airtime.return_value = False
    creditDetails = {'msisdn': '712306172', 'amount': 700.0}
>>>>>>> upstream/master
    with app.test_client() as app_test:
        headers = {
            'ContentType': 'application/json',
            'dataType': 'json',
<<<<<<< HEAD
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjMDg0YmVlMS1kNmE4LTRiZWYtOWE4OS1lMzRhYWQyZDg4NWQiLCJleHAiOjE1NDM5MTM5OTN9.KugSYwHDWW0cHnqCUzgXYbhVau5-3SXy2N2Av4TsPT0'
            
=======
            'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJs'
                              'aWNfaWQiOiI3ODM1MGFlMy0yYThiLTQzYmItYWVmMS02M'
                              'WE3YWI1NGM4ODUiLCJleHAiOjE1NDI3OTY1NTF9.4HCZN'
                              '00ppXyhg8KnkZ_mTABe-9q60Fw-bro3HlBUSR4'

>>>>>>> upstream/master
        }
        response = app_test.post(
            '/inservices/api/v1.0/airtime/credit',
            data=json.dumps(creditDetails),
            content_type='application/json',
            headers=headers

        )
        assert response.status_code == 500

<<<<<<< HEAD
=======
        assert response.status_code == 400
>>>>>>> upstream/master
