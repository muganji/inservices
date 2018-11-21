# Testing the credit/Debit airtime handler.
import unittest
from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none
from app.handlers.airtime_handler import creditAirtime,debitAirtime
class testCreditAirtimeMethods(unittest.TestCase):
    """
    The testCreditAirtimeMethods is a class that ontains all the proposed tests performed onto the debit and credit modules.
    """
    def test_isvalid_msid(self):
        """
        The test_isvalid_msid returns True if the submitted msid exists in the database.
        Argument = msidn
        """
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.msidnvalidity(22222),True)
    def test_invalid_msidn(self):
        """
        The test_invalid_msidn returns False if the submitted msid doesn't exist in the database.
        Argument = msidn
        """
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.msidnvalidity(22222),False)
    def test_isvalid_paying_account(self):
        """
        The test_isvalid_paying_account returns True if the submitted msid exists in the database.
        Argument = msidn
        """
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.paying_account(24422),True)
    def test_invalid_paying_account(self):
        """
        The test_invalid_paying_account returns True if the submitted msid exists in the database.
        Argument = msidn
        """
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.paying_account(24422),False)
    def test_balance_status(self):
        """
        The test_balance_status returns True if the submitted msid has balance greater than 0 on the wallet.
        """
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.check_Crediting_Account_Balance(24422)>0,True)
        self.assertEqual(creditairtime.check_Crediting_Account_Balance(24422)<=0,False)
    def test_account_bal_GTE(self):
        """
        The test_isvalid_returns True if the submitted msid exists in the database.
        Argument = msidn
        """
        creditairtime = creditAirtime()
        balance = 500
        self.assertEqual(creditairtime.check_isaccount_bal_GTE(24422,1000>=balance),True)
    def test_account_bal_LTE(self):
        """
        The test_account_bal_LTE True is the submitted msid exists in the database.
        Parm  = msidn
        """
        balance = 500
        creditairtime = creditAirtime()
        self.assertEqual(creditairtime.check_isaccount_bal_GTE(24422,300<=balance),True)
    def test_deduct_amount(self):
        creditairtime = creditAirtime()
        
        self.assertEqual(creditairtime.deduct_amount_from_msidn(10000),True)
class testDebitAirtimeMethods(unittest.TestCase):
    def test_msidn_isvalidity(self):
        debitairtime = debitAirtime()
        self.assertEqual(debitairtime.msidnvalidity(22222),True)
    def test_msidn_invalidity(self):
        debitairtime = debitAirtime()
        self.assertEqual(debitairtime.msidnvalidity(22222),False)
    #def test_msidn_balance_status(self):
        #debitairtime = debitAirtime()
        #self.assertTrue(debitairtime.msidn_balance_status(22222),True)
        #self.assertFalse(debitairtime.msidnvalidity(444),False)
    def test_debit_bal_GTE_Amount(self):
        """
        The test_isvalid_returns True if the submitted msid exists in the database.
        Argument = msidn
        """
        debitairtime = debitAirtime()
        balance = 500
        self.assertEqual(debitairtime.debit_isaccount_bal_GTE(24422,1000>=balance),True)
    def test_debit_bal_LTE_Amount(self):
        """
        The test_account_bal_LTE True is the submitted msid exists in the database.
        Parm X = msidn
        """
        balance = 500
        debitairtime = debitAirtime()
        self.assertEqual(debitairtime.debit_isaccount_bal_LTE(24422,300<=balance),True)

