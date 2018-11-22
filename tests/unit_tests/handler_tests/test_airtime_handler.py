# Testing the credit/Debit airtime handler.
import pytest


from app.handlers.profile import (
    account_balance,
    account_info,
    profile_status)
from app.handlers.airtime_handler import creditAirtime, debitAirtime

from app.models.user import User


def test_isvalid_msid():
    credit = creditAirtime()
    msisdn = '712306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.msidnvalidity(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_invalid_msidn():
    credit = creditAirtime()
    msisdn = '778306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.msidnvalidity(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_isvalid_paying_account():
    credit = creditAirtime()
    msisdn = '712306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.paying_account(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_invalid_paying_account():
    credit = creditAirtime()
    msisdn = '7783016172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.paying_account(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_balance_status():
    credit = creditAirtime()
    msisdn = '712306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.check_Crediting_Account_Balance(msisdn, current_user)

    # Assert
    assert isinstance(result, str)


def test_account_bal_GTE():
    credit = creditAirtime()
    msisdn = '712306172'
    amount = 2000.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.check_is_account_bal_GTE(msisdn, current_user, amount)

    # Assert
    assert isinstance(result, bool)


def test_account_bal_LTE():
    credit = creditAirtime()
    msisdn = '712306172'
    amount = 2000.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.check_is_account_bal_GTE(msisdn, current_user, amount)

    # Assert
    assert isinstance(result, bool)


def test_deduct_amount():
    credit = creditAirtime()
    msisdn = '712306172'
    amount = 100.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.deduct_amount_from_msidn(msisdn, current_user, amount)

    # Assert
    assert isinstance(result, str)

def test_credit_amount():
    credit = creditAirtime()
    msisdn = '712306172'
    amount = 100.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = credit.credit_msidn(msisdn, current_user, amount)

    # Assert
    assert isinstance(result, str)

def test_msidn_isvalidity():
    debitairtime = debitAirtime()
    msisdn = '712306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = debitairtime.msidnvalidity(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_msidn_invalidity():
    debitairtime = debitAirtime()
    msisdn = '778306172'
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = debitairtime.msidnvalidity(msisdn, current_user)

    # Assert
    assert isinstance(result, bool)


def test_debit_bal_GTE_Amount():
    debitairtime = debitAirtime()
    msisdn = '712306172'
    amount = 500.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = debitairtime.debit_is_account_bal_GTE(msisdn, current_user,amount)

    # Assert
    assert isinstance(result, bool)



def test_debit_bal_LTE_Amount():
    debitairtime = debitAirtime()
    msisdn = '712306172'
    amount = 500.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = debitairtime.debit_is_account_bal_LTE(msisdn, current_user,amount)

    # Assert
    assert isinstance(result, bool)


def test_debit_deduct_amount():
    debitairtime = debitAirtime()
    msisdn = '712306172'
    amount = 500.0
    current_user = User(mml_username='pkgmml', mml_password='pkgmml99')

    # Act
    result = debitairtime.deduct_amount(msisdn, current_user,amount)

    # Assert
    assert isinstance(result, bool)

    
