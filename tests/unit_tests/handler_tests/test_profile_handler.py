"""Profile handler unit tests.
"""
from intelecom.intelecom import MsisdnMatchError
import pytest

from app.handlers.profile_handler import (
    account_balance,
    account_info,
    profile_status
)
from app.models.user import User


def test_account_info_returns_dict():
    # Arrange
    msisdn = '711187734'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = account_info(msisdn, current_user)

    # Assert
    assert isinstance(result, dict)


def test_account_balance_returns_dict():
    # Arrange
    msisdn = '711187734'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = account_balance(msisdn, current_user)

    # Assert
    assert isinstance(result, dict)


def test_profile_status_returns_dict():
    # Arrange
    msisdn = '711187734'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = profile_status(msisdn, current_user)

    # Assert
    assert isinstance(result, dict)


def test_profile_status_raises_MsisdnMatchError_when_msisdn_not_exist():
    # Arrange
    msisdn = '721187734'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Assert
    with pytest.raises(MsisdnMatchError):
        profile_status(msisdn, current_user)
