"""Profile handler unit tests.
"""
from unittest.mock import Mock, patch
from intelecom.intelecom import INConnection, MsisdnMatchError
import pytest

from app.handlers.profile_handler import INRequestHandler
from app.models.user import User

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'display_account_info')
def test_account_info_returns_dict(mock_display_account_info, mock_login, mock_logout):
    # Arrange
    mock_msisdn = Mock()
    mock_current_user = Mock()
    mock_display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2019-03-12'
    }
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert isinstance(result, dict)

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'display_account_info')
def test_account_info_return_value(mock_display_account_info, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_current_user = Mock()
    mock_display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2019-03-12'
    }
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert result == {
        'mobileNumber': mock_msisdn,
        'balance': 12300.0,
        'subscriberProfile': '9',
        'status': 'ACTIVE'
    }

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'display_account_info')
def test_account_info_return_notactive_account(mock_display_account_info, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_current_user = Mock()
    mock_display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2018-03-12'
    }
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert result == {
        'mobileNumber': mock_msisdn,
        'balance': 12300.0,
        'subscriberProfile': '9',
        'status': 'NOT ACTIVE'
    }

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'debit_account')
def test_debit_airtime_success(mock_debit_account, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_amount = '5000'
    mock_current_user = Mock()
    mock_debit_account.return_value = True
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    success_result = prepaid_request.debit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert success_result

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'debit_account')
def test_debit_airtime_failure(mock_debit_account, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_amount = '5000'
    mock_current_user = Mock()
    mock_debit_account.return_value = False
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    success_result = prepaid_request.debit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert not success_result

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'credit_account')
def test_credit_airtime_success(mock_credit_account, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_amount = '5000'
    mock_current_user = Mock()
    mock_credit_account.return_value = True
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    success_result = prepaid_request.credit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert success_result

@patch.object(INConnection, 'logout')
@patch.object(INConnection, 'login')
@patch.object(INConnection, 'credit_account')
def test_credit_airtime_failure(mock_credit_account, mock_login, mock_logout):
    # Arrange
    mock_msisdn = '71187734'
    mock_amount = '5000'
    mock_current_user = Mock()
    mock_credit_account.return_value = False
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    success_result = prepaid_request.credit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert not success_result
