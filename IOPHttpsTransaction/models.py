from django.db import models
import threading
import urllib2
import requests
import re
from django.conf import settings

class IOPHttpsException(Exception): pass
class NoUrlException(IOPHttpsException):
    def __str__(self):
        return "Cannot instantiate InteracOnlineTransaction without a url:REQ_MALFORMED_URL:-1"
class EmptyRequestException(IOPHttpsException):
    def __str__(self):
        return "Cannot send InteracOnlineTransaction with an empty request:REQ_INVALID_REQUEST:-6"
class PostErrorException(IOPHttpsException):
    def __str__(self):
        return "Error during POST InteracOnlineTransaction request:REQ_POST_ERROR:-2"
class ResponseErrorException(IOPHttpsException):
    def __str__(self):
        return "Error getting response from POST InteracOnlineTransaction request:REQ_RESPONSE_ERROR:-4"
class EmptyResponseException(IOPHttpsException):
    def __str__(self):
        return "Error in processing response in InteracOnlineTransaction with an empty request:REQ_RESPONSE_ERROR:-4"
    
class InteracOnlineTransaction(models.Model):
    
    url = models.CharField(max_length=128, null=True, blank=True)
    cardtype = models.CharField(max_length=32)
    transactionid = models.IntegerField(11)
    hostedsolnid = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=32)
    appcode = models.CharField(max_length=32, null=True, blank=True)
    respcode = models.IntegerField(11, null=True, blank=True)
    message = models.CharField(max_length=64, null=True, blank=True)
    issname = models.CharField(max_length=32, null=True, blank=True)
    issconf = models.CharField(max_length=32, null=True, blank=True)
    requested_amount = models.DecimalField(decimal_places=2,
                                 max_digits=settings.DECIMAL_DIGITS_MAX)
    amount = models.DecimalField(decimal_places=2,
                                 max_digits=settings.DECIMAL_DIGITS_MAX)
    fee = models.DecimalField(decimal_places=2,
                                 max_digits=settings.DECIMAL_DIGITS_MAX, blank=True, null=True)
    transdate = models.DateTimeField(null=True, blank=True)
    verifiedsuccess = models.BooleanField(default=False)
    verifiedreject = models.BooleanField(default=False)
    
        
    @classmethod
    def create(cls, url=None, cardtype=None, transactionid=None, hostedsolnid=None, status=None, appcode=None, respcode=None, message=None, issname=None, issconf=None, transdate=None, requested_amount=None, amount=None, fee=None):
        req = None
        timeout = 60000
        if url == None:
            raise NoUrlException
        if transdate:
            transdate = re.sub('/','-',transdate)
        
        iop = cls(url=url, cardtype=cardtype, transactionid=transactionid, hostedsolnid=hostedsolnid, status=status, appcode=appcode, respcode=respcode, message=message, issname=issname, issconf=issconf, transdate=transdate, requested_amount=requested_amount, amount=amount, fee=fee)
        return iop
        
    def complete(self):
        self.verifiedsuccess = True;
        self.save()
    
    def reject(self):
        self.verifiedreject = True;
        self.save()
    
    def purchase(self, merchantId, storeId, apiToken, track2, invoice, amount):
        self.req={'txnType':'Purchase', 'merchantId':merchantId, 'storeId':storeId, 'apiToken':apiToken, 'track2':track2, 'invoice':invoice, 'amount':abs(amount)}
        return self.process_transaction()

    def refund(self, merchantId, storeId, apiToken, transactionId, amount):
        self.req={'txnType':'Refund', 'merchantId':merchantId, 'storeId':storeId, 'apiToken':apiToken, 'transactionId':transactionId, 'amount':abs(amount)}
        return self.process_transaction()

    def verify(self, merchantId, storeId, apiToken, transactionId):
        self.req={'txnType':'Verify', 'merchantId':merchantId, 'storeId':storeId, 'apiToken':apiToken, 'transactionId':transactionId}
        return self.process_transaction()

    def process_transaction(self):
        receipt = None
        resp = None
        data = None
        if self.req == None:
            raise EmptyRequestException
        # send POST request to the server
        try:
            httprequest = requests.post(self.url,self.req)
        except Exception, e:
            raise PostErrorException
        # check the response
        try:
            if httprequest.status_code == requests.codes.ok:
                receipt = TransactionResponse(httprequest.text)
            else:
                raise PostErrorException
        except Exception, e:
            raise ResponseErrorException
        
        return receipt
        

class TransactionResponse:

    def __init__(self,data=None):
        self.cardType = None
        self.txnAmount = '0.0'
        self.txnId = '0'
        self.txnType = None
        self.txnData = None
        self.respCode = -1
        self.isoCode = None
        self.authCode = None
        self.message = None
        self.isComplete = False
        self.isTimeout = False
        if data == None:
            raise EmptyResponseException
        else:
           self.format(data)
        

    def format(self,data):
        param = {}
        lines = data.split(';')
        
        for l in lines:
            paramKey,paramValue = l.split('=')
            param[paramKey] = paramValue
            
        if param.get("cardType"):
            self.cardType = param["cardType"]
            
        if param.get("txnId"):
            self.txnId = param["txnId"]
            
        if param.get("txnAmount"):
            self.txnAmount = param["txnAmount"]
            
        if param.get("txnType"):
            self.txnId = param["txnType"]
            
        if param.get("txnData"):
            self.txnData = param["txnData"]
            
        if param.get("respCode"):
            self.respCode = param["respCode"]
            
        if param.get("isoCode"):
            self.isoCode = param["isoCode"]
            
        if param.get("authCode"):
            self.authCode = param["authCode"]
            
        if param.get("message"):
            self.message = param["message"]
            
        if param.get("isComplete"):
            self.isComplete = param["isComplete"]
            
        if param.get("isTimeout"):
            self.isTimeout = param["isTimeout"]
            

    def getCardType(self):
        return self.cardType
    
    def getTxnAmount(self):
        return self.txnAmount
    
    def getTxnId(self):
        return self.txnId
    
    def getTxnType(self):
        return self.txnType
    
    def getTxnData(self):
        return self.txnData
    
    def getRespCode(self):
        return self.respCode
    
    def getIsoCode(self):
        return self.isoCode
    
    def getAuthCode(self):
        return self.authCode
    
    def getMessage(self):
        return self.message
    
    def isComplete(self):
        return self.isComplete
    
    def isTimeout(self):
        return self.isTimeout
    

