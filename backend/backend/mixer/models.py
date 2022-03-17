from django.db import models


class Deposit(models.Model):
    '''
    The desposit table represents unique desposit address to which user deposit the money =.
    '''
    deposit_address = models.TextField(null=False, blank=False, unique=True)
    deposited_amount = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=False, default=0.0)
    after_fee_amount = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=False, default=0.0)
    processed_amount = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=False, default=0.0)
    pooled = models.BooleanField(default=False)
    transfer_complete = models.BooleanField(default=False)
    no_of_transactions = models.IntegerField(null=True, blank=False, default=10)
    created_at = models.DateTimeField(auto_now_add=True)


class DestinationAddress(models.Model):
    '''
    This table store the destination address for desposit address.
    This table might conatin multiple destination address per deposit address.
    | deposit_address          | destination_address      |
    | c1                       | d1                       |
    | c1                       | d2                       |    
    '''
    deposit_address = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    destination_address = models.TextField(null=False, blank=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deposit_address', 'destination_address'], name='unique_deposit_des_address')
        ]


class ProcessedTransaction(models.Model):
    '''
    Transactions that have already been processed and some part of amount is desposited into destniation table
    '''
    destination_address = models.ForeignKey(DestinationAddress, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=8, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
