# The airtime_handler.py handles the business logic that comprises of crediting and debiting airtime to a valid MSIDN.
import os

class creditAirtime(object):
    def msidnvalidity(self, msidn):
        """
        The msidnValidity method checks whether the supplied msidn exists, returns True if yes and False otherwise.
        argument = a msidn of a client or agent.
        return status either True or False.
        """
        # TODO Must be implement to be querried from the database file..
        
        self.status =False
        if msidn.exist():
            self.status = True
        else:
            self.status = False
            print('This ',msidn ,'to be credited does not exist')
        return self.status
         #len(profile.query.filter_by(msidn=msidn).all()) <1 
      
            
    def paying_account(self,msidn):
        # TODO Must be implement to be querried from the database file..
        self.status =False
        if msidn.exist():
            self.status = True
        else:
            self.status = False
            print('This paying account number',msidn ,'does not exist')
        #self.status
        return self.status
        
    def check_Crediting_Account_Balance(self,msidn):
        _accounts =[]
        for acct, i in _accounts:
            if msidn ==i:
                return acct.balance,
            return True

        return
    def check_isaccount_bal_GTE(self,msidn,amount):
        accounts = {}
        

        return
    def check_isaccount_bal_LTE(self,msidn,amount):
        return
    def deduct_amount_from_msidn(self,amount):
        return
    def credit_msidn(self,msidn,amount):
        return
class debitAirtime(object):
    def msidnvalidity(self, msidn):
        self.status =False
        if msidn.exist():
            self.status = True
        else:
            self.status = False
            print('This ',msidn ,'to be credited does not exist')
        return self.status
        
    def msidn_balance_status(self,msidn):
        pass
    def deduct_amount(self,amount):
        pass
    def debit_isaccount_bal_GTE(self,msidn,amount):
        return 
    def debit_isaccount_bal_LTE(self,msidn,amount):
        return
    
    