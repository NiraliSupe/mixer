import posix
import posixpath
from .config import API_BASE_URL
import requests    
from enum import Enum
from rest_framework.exceptions import APIException

class NoDataException(APIException):
    status_code = 404
    default_detail = {"deatil": "Must provide data to post."}

class JobcoinApiException(APIException):
    status_code = 404
    default_detail = {"deatil": "Must provide data to post."}

# Write your Jobcoin API client here.
class JobcoinEndpoint(Enum):
    ADDRESSES = 'addresses'
    TRANSACTIONS = 'transactions'

    def __str__(self):
        return self.value

class JobcoinApi:
    @classmethod
    def get(cls, endpoint, value=None):
        if not isinstance(endpoint, JobcoinEndpoint):
            raise Exception('Jobcoin endpoint must be a type of JobcoinEndpoint.')

        api_base = posixpath.join(API_BASE_URL, endpoint.value)

        if value:
            response =  requests.get(f'{api_base}/{value}')
        else:
            response = requests.get(api_base)
    
        if response.status_code != 200:
            raise JobcoinApiException(response.text)

        return response.json()

    @classmethod
    def post(cls, endpoint, json_data):
        if not isinstance(endpoint, JobcoinEndpoint):
            raise Exception('Jobcoin endpoint must be a type of JobcoinEndpoint.')

        api_base = posixpath.join(API_BASE_URL, endpoint.value)

        if json_data:
            response =  requests.post(api_base, json=json_data)
        else:
            raise NoDataException({"deatil": "Must provide data to post: Required fields: fromAddress, toAddress and amount."})

        if response.status_code != 200:
            raise JobcoinApiException(response.text)

        return response.json()
