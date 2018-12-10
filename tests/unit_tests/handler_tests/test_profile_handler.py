"""Profile handler unit tests.
"""
from unittest import mock
from intelecom.intelecom import INConnection, MsisdnMatchError
import pytest

from app.handlers.profile_handler import INRequestHandler
from app.models.user import User


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_account_info_returns_dict(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_inconnection_enter.return_value.display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2019-03-12'
    }
    mock_inconnection_exit.return_value = None
    mock_msisdn = mock.ANY
    mock_current_user = mock.Mock()
    prepaid_request = INRequestHandler(None, None, None)

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert isinstance(result, dict)


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_account_info_return_value(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_inconnection_exit.return_value = None
    mock_msisdn = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2019-03-12'
    }
    prepaid_request = INRequestHandler(None, None, None)

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert result == {
        'mobileNumber': mock_msisdn,
        'balance': 12300.0,
        'subscriberProfile': '9',
        'status': 'ACTIVE'
    }


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_account_info_return_notactive_account(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_inconnection_exit.return_value = None
    mock_msisdn = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.display_account_info.return_value = {
        'ACCLEFT': '12300',
        'SUBSCRIBERTYPE': '9',
        'ACNTSTAT': '1',
        'CALLSERVSTOP': '2018-03-12'
    }
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    result = prepaid_request.account_info(mock_msisdn, mock_current_user)

    # Assert
    assert result == {
        'mobileNumber': mock_msisdn,
        'balance': 12300.0,
        'subscriberProfile': '9',
        'status': 'NOT ACTIVE'
    }


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_debit_airtime_success(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_inconnection_exit.return_value = None
    mock_msisdn = mock.ANY
    mock_amount = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.debit_account.return_value = True
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.debit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert success_result


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_debit_airtime_failure(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_amount = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.debit_account.return_value = False
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.debit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert not success_result


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_credit_airtime_success(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_amount = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.credit_account.return_value = True
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.credit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert success_result


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_credit_airtime_failure(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_amount = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.credit_account.return_value = False
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.credit_airtime(
        mock_msisdn,
        mock_amount,
        mock_current_user)

    # Assert
    assert not success_result


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_purchase_package_returns_dict(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_package_type = mock.ANY
    mock_package_grade = mock.ANY
    mock_profile = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.purchase_package.return_value = True
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.purchase_package(
        msisdn=mock_msisdn,
        current_profile=mock_profile,
        package_type=mock_package_type,
        current_user=mock_current_user,
        package_grade=mock_package_grade)

    # Assert
    assert isinstance(success_result, dict)


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_purchase_package_return_value(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_package_type = mock.ANY
    mock_package_grade = mock.ANY
    mock_profile = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.purchase_package.return_value = True
    mock_host = '172.18.0.2'
    mock_port = 7090
    mock_buffer_size = 4096
    prepaid_request = INRequestHandler(
        host=mock_host,
        port=mock_port,
        buffer_size=mock_buffer_size)

    # Act
    success_result = prepaid_request.purchase_package(
        msisdn=mock_msisdn,
        current_profile=mock_profile,
        package_type=mock_package_type,
        current_user=mock_current_user,
        package_grade=mock_package_grade)

    # Assert
    assert success_result == {
        'operationResult': 'OK',
        'msisdn': mock_msisdn,
        'packageType': mock_package_type,
        'packageGrade': mock_package_grade
    }


@mock.patch.object(INConnection, '__exit__')
@mock.patch.object(INConnection, '__enter__')
def test_purchase_package_failed(
    mock_inconnection_enter,
    mock_inconnection_exit
):
    # Arrange
    mock_msisdn = mock.ANY
    mock_package_type = mock.ANY
    mock_package_grade = mock.ANY
    mock_profile = mock.ANY
    mock_current_user = mock.Mock()
    mock_inconnection_enter.return_value.purchase_package.return_value = False
    prepaid_request = INRequestHandler(
        None,
        None,
        None
    )

    # Act
    success_result = prepaid_request.purchase_package(
        msisdn=mock_msisdn,
        current_profile=mock_profile,
        package_type=mock_package_type,
        current_user=mock_current_user,
        package_grade=mock_package_grade)

    # Assert
    assert success_result == {
        'operationResult': 'FAILED',
        'msisdn': mock_msisdn,
        'packageType': mock_package_type,
        'packageGrade': mock_package_grade
    }
