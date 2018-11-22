# The airtime_handler.py handles the business logic that comprises of crediting and debiting airtime to a valid MSIDN.
from intelecom.intelecom import INConnection

from app import app

from app.handlers.profile import account_balance, account_info, profile_status


from app.models.user import User


class creditAirtime():
    def msidnvalidity(self, msidn: str, current_user: User) -> bool:
        """
        The msidnValidity method checks whether the supplied msidn exists, returns True if yes and False otherwise.
        argument = a msidn of a client or agent.
        return status either True or False.
        """
        isValid = False
        userProfile = profile_status(msidn, current_user)
        if msidn in iter(userProfile.values()):
            isValid = True
        else:
            print("The supplied ",msidn," doesn't exist in the database.")
            isValid = False
        return isValid


    def paying_account(self,msidn: str, current_user: User) -> bool:
        isValid =False
        userProfile = profile_status(msidn, current_user)
        if msidn in iter(userProfile.values()):
            isValid = True
        else:
            isValid = False
            print('This paying account number',msidn ,'does not exist')
        return isValid


    def check_Crediting_Account_Balance(self, msidn: str, current_user: User) -> str:
        acc = account_balance(msidn, current_user)
        balance: str
        if msidn in iter(acc.values()):
            balance = acc.get('balance')
        else:
            print("The supplied ",msidn," doesn't have balance.")
        return balance

    def check_is_account_bal_GTE(self, msidn: str, current_user: User, amount: float) -> bool:
        isBalanceGTE = False
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            if acc['balance'] >= amount:
                isBalanceGTE = True
            else:
                isBalanceGTE = False
        return isBalanceGTE
        
    def check_is_account_bal_LTE(self,msidn: str, current_user: User,amount: float) -> bool:
        isBalanceLTE = False
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            if acc['balance'] <= amount:
                isBalanceLTE = True
            else:
                isBalanceLTE = False
        return isBalanceLTE
        

    def deduct_amount_from_msidn(self,msidn: str, current_user: User,amount: float) -> str:
        newBalance: float
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            balance = float(acc.get('balance'))
            newBalance = balance - amount
            balToString = acc['balance'] = newBalance
            return balToString
        else:
            print('We only debit a valid msidn')
        return

    def credit_msidn(self,msidn: str, current_user: User,amount: float) -> str:
        newBalance: float
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            balance = float(acc.get('balance'))
            newBalance = balance + amount
            balToString = acc['balance'] = newBalance
            return balToString
        else:
            print('We only debit a valid msidn')
        return


class debitAirtime():
    def msidnvalidity(self, msidn: str, current_user: User) -> bool:
        isValid = False
        userProfile = profile_status(msidn, current_user)
        if msidn in iter(userProfile.values()):
            isValid = True
        else:
            print("The supplied ",msidn," doesn't exist in the database.")
            isValid = False
        return isValid
        
    def msidn_balance_status(self,msidn: str, current_user: User) -> float:
        acc = account_balance(msidn, current_user)
        balance: str
        if msidn in iter(acc.values()):
            balance = acc.get('balance')
        else:
            print("The supplied ",msidn," doesn't have balance.")
        return balance

    def deduct_amount(self,msidn: str, current_user: User,amount: float)-> float:
        newBalance: float
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            balance = float(acc.get('balance'))
            newBalance = balance - amount
            balToString = acc['balance'] = newBalance
            return balToString
        else:
            print('We only debit a valid msidn')
        return


    def debit_is_account_bal_GTE(self,msidn: str, current_user: User,amount: float) -> bool:
        isBalanceGTE = False
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            if acc['balance'] >= amount:
                isBalanceGTE = True
            else:
                isBalanceGTE = False
        return isBalanceGTE


def debit_is_account_bal_LTE(self,msidn: str, current_user: User,amount: float) -> bool:
        isBalanceLTE = False
        acc = account_balance(msidn, current_user)
        if msidn in iter(acc.values()):
            if acc['balance'] <= amount:
                isBalanceLTE = True
            else:
                isBalanceLTE = False
        return isBalanceLTE