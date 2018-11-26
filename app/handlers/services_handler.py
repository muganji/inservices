"""Service package purchases handler
"""
from intelecom.intelecom import INConnection

from app import app
from app.models.user import User


def purchase_package(
        msisdn: str,
        current_user: User,
        package_type: str,
        package_grade: str = None
        ) -> dict:
    """[summary]

    Parameters
    ----------
    msisdn : str
        Mobile number purhasing the package.
    package_type : str
        Packge type being purchased.
    package_grade : str -- [description] (default: {None})

    Returns
    -------
    dict
        Details of MSISDN, packageType, packageGrade, ProfileBefore,
        profileAfter returned.
    """
    with INConnection(
            app.config['IN_SERVER']['HOST'],
            current_user.mml_username,
            current_user.mml_password,
            app.config['IN_SERVER']['PORT'],
            app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        # Collect account information befor package purchase.
        network_account_info = dict(
            in_connection.display_account_info(msisdn)
        )

        profile_before = network_account_info['SUBSCRIBERTYPE']
        balance_before = network_account_info['ACCTLEFT']

        package_purchased = in_connection.purchase_package(
            msisdn,
            package_type,
            package_grade
        )

        # Collect account information after package purchase.
        network_account_info = dict(
            in_connection.display_account_info(msisdn)
        )

        if package_purchased:
            operation_result = 'OK'
            profile_after = network_account_info['SUBSCRIBERTYPE']
            balance_before = network_account_info['ACCTLEFT']
        else:
            operation_result = 'FAILED'
            profile_after = network_account_info['SUBSCRIBERTYPE']
            balance_after = network_account_info['ACCTLEFT']

        return {
            'operationResult': operation_result,
            'msisdn': msisdn,
            'balanceBefore': balance_before,
            'profileBefore': profile_before,
            'balanceAfter': balance_after,
            'profileAfter': profile_after
        }
