import uuid
import jwt
from datetime import datetime, timedelta


from intelecom.intelecom import INConnection


from app.inservices import app
from app.models.user import User


def airtime_credit(msisdn: str, amount: str, current_user: User) -> bool:
    """Credit airtime account"""

    # Open connection to the IN.
    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        account_credit_succeeeded = in_connection.credit_account(
            msisdn,
            amount, 
            'WEBSMAP_{0}'.format(current_user.username))

        # If msisdn credit succeeded return success code.
        if account_credit_succeeeded:
            return True
        else:
            return False
