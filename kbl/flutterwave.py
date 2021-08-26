from dotenv import load_dotenv
import os, hashlib, warnings, requests, json
import base64
from Cryptodome.Cipher import DES3
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


class FlutterWave(object):
    
    baseUrl = "https://api.ravepay.co/flwv3-pug/getpaidx/api/"

    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a parameter."""

    def __init__(self, cardno=None, cvv=None, expirymonth=None, expiryyear=None, pin=None, amount=None, user=None):
        self.cardno = cardno
        self.cvv = cvv
        self.expirymonth = expirymonth
        self.expiryyear = expiryyear
        self.pin = pin
        self.amount = amount
        self.user = user

    def getKey(self,secret_key):
        hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""

    def encryptData(self, key, plainText):
        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, hence the need for the conversion below
        test = plainText.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted

    def getRef(self):
        return 'FUZ-PAYREF-'+str(uuid.uuid1())[:12]


    def pay_via_card(self):
        data = {
            'PBFPubKey': os.environ.get('FLUTTERWAVE_PUBLIC'),
            "cardno": self.cardno,
            "cvv": self.cvv,
            "expirymonth": self.expirymonth,
            "expiryyear": self.expiryyear,
            "currency": "NGN",
            "country": "NG",
            'suggested_auth': 'PIN',
            'pin': self.pin,
            "amount": self.amount,
            'txRef': self.getRef(),
            "email": self.user.email,
            "phonenumber": self.user.phone,
            "firstname": self.user.first_name,
            "lastname": self.user.last_name,
        }

        sec_key = os.environ.get('FLUTTERWAVE_SECRET')
        # hash the secret key with the get hashed key function
        hashed_sec_key = self.getKey(sec_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

        encrypt_3DES_key = self.encryptData(hashed_sec_key, json.dumps(data))

        # payment payload
        payload = {
            "PBFPubKey": os.environ.get('FLUTTERWAVE_PUBLIC'),
            "client": encrypt_3DES_key,
            "alg": "3DES-24"
        }

        # card charge endpoint
        endpoint = FlutterWave.baseUrl+"charge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        #print(response.json())
        return response.json()

    
    '''
    ### Validate payment with OTP
    '''
    def validatePayment(self, ref, otp):
        data = {
            "otp": otp,
            "transaction_reference": ref,
            'PBFPubKey': os.environ.get('FLUTTERWAVE_PUBLIC')
        }

        # validation endpoint
        endpoint = FlutterWave.baseUrl+'validatecharge'

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        #print(response.json())

        return response.json()



    '''
    ### Verify payment
    '''
    def verifyPayment(self, txRef, amount):
        data = {
            "txref": txRef,
            "SECKEY": os.environ.get('FLUTTERWAVE_SECRET')
        }

        # validation endpoint
        endpoint = FlutterWave.baseUrl+'v2/verify'

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        data = response.json()
        
        if 'status' in data and data['status'] == "success":
            return data['data']['amount'] == amount

        return False


   