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
@patch.object(INConnection, 'account_info')
def test_msisdn_status(mock_account_info, mock_login, mock_logout, mock_token, mock_user):
    """
    Testing the msisdn profile status and balance.
    """
    msisdn = '712306172'
    mock_token.return_value = {
        'public_id': 'public_id=f974c6bb-862d-4138-9fe4-b3ea1b70c7d2'
    }
    with app.test_client() as test_app:
        response = test_app.get(
            '/inservices/api/v1.0/profile/status',
            data = msisdn
        )

    return response.status_code == 200