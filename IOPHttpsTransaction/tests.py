"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from virex.IOPHttpsTransaction import models
from virex.IOPHttpsTransaction.models import IOPHttpsException, NoUrlException, EmptyRequestException, PostErrorException, ResponseErrorException, EmptyResponseException


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class IOPHttpsTestCase(TestCase):
    def test_new_instance_no_url(self):
        with self.assertRaises(NoUrlException):
            IOP = models.InteracOnlineTransaction.create()
        
    def test_verify_no_req(self):
        with self.assertRaises(TypeError):
            url = 'thisurl'
            IOP = models.InteracOnlineTransaction.create(url)
            IOP.verify()
        
    def test_verify_req_badurl(self):
        with self.assertRaises(PostErrorException):
            url = 'thisurl'
            IOP = models.InteracOnlineTransaction.create(url)
            merchantId = 1
            storeId = 2
            apiToken = 3
            transactionId = 4
            IOP.verify(merchantId, storeId, apiToken, transactionId)
        
class TransactionResponseTestCase(TestCase):
    def test_data_load(self):
        indata = 'cardType=thiscard;tsnAmount=5.00;txnId=1;txnType=what;txnData=what'
        Response = models.TransactionResponse(indata)
        mycard = Response.getCardType()
        self.assertEqual(mycard,'thiscard')
        
    def test_data_load_noauthCode(self):
        indata = 'cardType=thiscard;tsnAmount=5.00;txnId=1;txnType=what;txnData=what'
        Response = models.TransactionResponse(indata)
        mycard = Response.getAuthCode()
        self.assertEqual(mycard,None)
        