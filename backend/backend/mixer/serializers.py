from rest_framework import serializers
from mixer.models import Deposit, ProcessedTransaction, DestinationAddress


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
         model  =  Deposit
         fields =  '__all__'


class DestinationAddressSerializer(serializers.ModelSerializer):
    class Meta:
         model  =  DestinationAddress
         fields =  '__all__'


class ProcessedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
         model  =  ProcessedTransaction
         fields =  '__all__'
