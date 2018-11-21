"""Core handler unit tests.
"""
from app.handlers.core import msisdn_is_valid


def test_msisdn_is_valid_returns_bool():
    # Arrange
    msisdn = '711187734'

    # Act
    result = msisdn_is_valid(msisdn)

    # Assert
    assert isinstance(result, bool)


def test_msisdn_is_valid_when_valid_msisdn_returns_True():
    # Arrange
    msisdn = '711187734'

    # Act
    valid = msisdn_is_valid(msisdn)

    # Assert
    assert valid


def test_msisdn_is_valid_when_invalid_msisdn_returns_True():
    # Arrange
    msisdn = '721187734'

    # Act
    valid = msisdn_is_valid(msisdn)

    # Assert
    assert not valid
