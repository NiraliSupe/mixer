from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime
import time
import random
from .jobcoin.jobcoin import JobcoinApi, JobcoinEndpoint
from mixer.models import Deposit, ProcessedTransaction, DestinationAddress
from django.conf import settings
from decimal import Decimal

# To do: add transaction atomic
@shared_task(name = "send_to_house_address")
def send_to_house_address(*args, **kwargs):  
    address_processed = []

    for address in Deposit.objects.filter(pooled=False):  

        transaction = JobcoinApi.get(JobcoinEndpoint.ADDRESSES, address.deposit_address)

        if transaction['balance']:
            for transaction in transaction['transactions']:
                if transaction['toAddress'] == address.deposit_address:
                    after_fee_amount = get_after_fee_amount(Decimal(transaction['amount'])).normalize()
                    json_data =  {
                        'fromAddress' : address.deposit_address,
                        'toAddress' : settings.HOUSE_ADDRESS,
                        'amount' : str(after_fee_amount)
                    }

                    JobcoinApi.post(JobcoinEndpoint.TRANSACTIONS, json_data)
                    
                    address_processed.append(address.deposit_address)
                    address.deposited_amount = transaction['amount']
                    address.after_fee_amount = after_fee_amount
                    address.pooled = True
                    address.save()
 
    if address_processed:   
        print(f"Address whose amount transfered to house address: {','.join(address_processed)}")
    else:
        print('No addresses proccessed')

def get_after_fee_amount(deposit_amount):
    return deposit_amount - round(deposit_amount * settings.MIXER_FEE, 8)

@shared_task(name = "mixer")
def mixer():
    desposits = Deposit.objects.filter(pooled=True, transfer_complete=False)

    for deposit in desposits:
        destinations = DestinationAddress.objects.filter(deposit_address=deposit)
        random_destination_address = random.choice(destinations)

        if deposit.no_of_transactions == 1:
            amount_to_credit = (deposit.after_fee_amount - deposit.processed_amount).normalize()
        else:
            amount_to_credit = credit_amount(deposit.after_fee_amount - deposit.processed_amount).normalize()

        json_data =  {
              'fromAddress' : settings.HOUSE_ADDRESS,
              'toAddress' : random_destination_address.destination_address,
              'amount' : str(amount_to_credit)
          }
        JobcoinApi.post(JobcoinEndpoint.TRANSACTIONS, json_data)
        insert_processed_transaction(random_destination_address ,amount_to_credit)
        deposit.no_of_transactions -= 1
        deposit.processed_amount += amount_to_credit
        if deposit.processed_amount == deposit.after_fee_amount:
          deposit.transfer_complete = True
        deposit.save()

def credit_amount(amount):
    credit_percent = Decimal(round(random.uniform(0.1, 0.5), 2))
    return round(amount * credit_percent, 8)

def insert_processed_transaction(destination_address, amount):
    processed_transaction = ProcessedTransaction(
      destination_address = destination_address,
      amount=amount,
      created_at=datetime.utcnow()
    )
    processed_transaction.save()