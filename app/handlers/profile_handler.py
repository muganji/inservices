"""IN subscriber profile handling module
"""
import logging
from datetime import datetime

from intelecom.intelecom import INConnection

from app.inservices import app
from app.handlers.core_handler import write_log
from app.models.user import User


def profile_status(msisdn: str, current_user: User) -> dict:
    """Returns the status of MSISDN account profile on the IN.

    Parameters
    ----------
    msisdn : str
        MSISDN number for the account whose status is being queried.

    current_user : User
        User performing the profile status query.

    Returns
    -------
    dict
        Details the status of the MSISDN.
    """
    with INConnection(
            app.config['IN_SERVER']['HOST'],
            current_user.mml_username,
            current_user.mml_password,
            app.config['IN_SERVER']['PORT'],
            app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        profile_info = dict(in_connection.display_account_info(msisdn))
        account_status = int(profile_info['ACNTSTAT'])
        temporary_suspend_date = datetime.strptime(
            profile_info['CALLSERVSTOP'],
            '%Y-%m-%d'
        )

        status_info = {
            'mobileNumber': msisdn
        }

        temporarily_suspended = (temporary_suspend_date < datetime.today())
        if account_status == 1 and not temporarily_suspended:
            status_info['status'] = 'ACTIVE'

        status_info['status'] = 'INACTIVE'

        # Log the status information returned.
        status_info_results = ' '\
            .join('{!s}={!s}'
                  .format(key, val) for (key, val) in status_info.items())
        write_log(
            logging.INFO,
            'API',
            'SYSTEM',
            f"IN QUERY RESULT=0 {status_info_results}",
            current_user.username
        )

        return status_info


def account_balance(msisdn: str, current_user: User) -> dict:
    """Get the balance on MSISDN account.

    Parameters
    ----------
    msisdn : str
        MSISDN number for the account whose balance is being required.

    current_user : User
        User performing the profile status query.

    Returns
    -------
    dict
        Transaction details and the balance of the account.
    """
    with INConnection(
            app.config['IN_SERVER']['HOST'],
            current_user.mml_username,
            current_user.mml_password,
            app.config['IN_SERVER']['PORT'],
            app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        profile_info = dict(in_connection.display_account_info(msisdn))
        balance = float(profile_info['ACCLEFT'])

        profile_balance = {
            'mobileNumber': msisdn,
            'balance': balance
        }

        # Log the balance information returned.
        profile_balance_results = ' '\
            .join('{!s}={!s}'
                  .format(key, val) for (key, val) in profile_balance.items())

        write_log(
            logging.INFO,
            'API',
            'SYSTEM',
            f"IN QUERY RESULT=0 {profile_balance_results}",
            current_user.username
        )

        return profile_balance


def account_info(msisdn: str, current_user: User) -> dict:
    """Get the MSISDN account information.

    Parameters
    ----------
    msisdn : str
        MSISDN number for the account whose account information is being
        required.

    current_user : User
        User performing the profile status query.

    Returns
    -------
    dict
        Transaction details and the account information.
    """
    with INConnection(
            app.config['IN_SERVER']['HOST'],
            current_user.mml_username,
            current_user.mml_password,
            app.config['IN_SERVER']['PORT'],
            app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        profile_info = dict(in_connection.display_account_info(msisdn))
        balance = float(profile_info['ACCLEFT'])
        subscriber_type = profile_info['SUBSCRIBERTYPE']
        account_status = int(profile_info['ACNTSTAT'])
        temporary_suspend_date = datetime.strptime(
            profile_info['CALLSERVSTOP'],
            '%Y-%m-%d'
        )

        profile_info = {
            'mobileNumber': msisdn,
            'balance': balance,
            'subscriberProfile': subscriber_type
        }

        temporarily_suspended = (temporary_suspend_date < datetime.today())
        if account_status == 1 and not temporarily_suspended:
            profile_info['status'] = 'ACTIVE'

        profile_info['status'] = 'INACTIVE'

        # Log the account information returned.
        profile_info_results = ' '\
            .join('{!s}={!s}'
                  .format(key, val) for (key, val) in profile_info.items())

        write_log(
            logging.INFO,
            'API',
            'SYSTEM',
            f"IN QUERY RESULT=0 {profile_info_results}",
            current_user.username
        )

        return profile_info
