from rest_framework import serializers
from .models import KYC

class KYCSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=KYC
        fields= '__all__'

    def create(self, validated_data):
        kyc = KYC(**validated_data)
        
        kyc.save()
        return kyc

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model=KYC
        fields=['email']