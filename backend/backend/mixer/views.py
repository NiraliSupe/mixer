from email.policy import default
from sys import exc_info
from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from django.http import HttpResponse
from mixer.models import Deposit, ProcessedTransaction, DestinationAddress
from mixer.serializers import DepositSerializer, ProcessedTransactionSerializer, DestinationAddressSerializer
from rest_framework.exceptions import APIException
import string, random
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db import transaction, IntegrityError
from datetime import datetime
#import backend.jobcoin

class NoParamException(APIException):
    status_code = 400
    default_detail = {"deatil": "Must supply required param."}


class InternalServerException(APIException):
    status_code = 500
    default_detail = {"deatil": "Interal Server Error. Please contact administration"}


class MixerAddress(APIView):
    def post(self, request):
        addresses = request.data.get('addresses', None)
        ## to do check if addresses here of type list
        if not addresses:
            raise NoParamException({"deatil": "Must supply destination addresses."})

        deposit_address = self.create_deposit_address_to_dest_address_rel(addresses)
 
        return Response({'deposit_address': deposit_address})

    def get_new_deposit_address(self):
        '''
        Creates a random string to act as a deposit address
        '''
        deposit_address = get_random_string(settings.DEPOSIT_ADDRESS_LENGTH, allowed_chars=string.ascii_uppercase + string.digits)

        while Deposit.objects.filter(deposit_address=deposit_address).exists():
            deposit_address = get_random_string(settings.DEPOSIT_ADDRESS_LENGTH, allowed_chars=string.ascii_uppercase + string.digits)
        
        return deposit_address

    @transaction.atomic
    def create_deposit_address_to_dest_address_rel(self, addresses):
        '''
        Given a list of addresses 
        Assign these addresses to be the payment addresses for a creditor
        and return a deposit address for that creditor.
        '''
        deposit_address = self.get_new_deposit_address()

        try:
            with transaction.atomic():
                no_of_transactions = max(settings.NO_OF_TRANSACTIONS, len(addresses)+2)
                deposit_obj = Deposit.objects.create(deposit_address=deposit_address, created_at=datetime.utcnow(), no_of_transactions=no_of_transactions)
                for address in addresses:
                    dest_add = DestinationAddress(
                        deposit_address = deposit_obj,
                        destination_address = address
                    )
                    dest_add.save()
        except  Exception as ex:
            transaction.set_rollback(True)
            raise InternalServerException({"details": "Interal Server Error. Please contact administration"})
            
        return deposit_address
