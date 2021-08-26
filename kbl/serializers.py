from kbl.models import payment
from kbl.models.policy import get_pol_num
from rest_framework import serializers
from .models import ( InsuredProfile, Product,User, MotorThirdPartyPolicy, 
    MotorComprehensivePolicy, Policy, MotorClaim, HomeXtra, Item, Injured, Payment,
    PushNotificationToken, PushNotification,Branch, Certificate, History, VehicleModel)
from kbl import models


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=PushNotificationToken
        fields=['token']

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        fields= ['url','email', 'password', 'first_name', 'last_name', 'phone', 'address', 'pk', 'profile_image', 'referrer' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        password = validated_data.pop('password')

        email = validated_data.pop('email')
        user = User(is_staff=False, is_superuser=False, is_active=True, email=email.lower(), **validated_data)
        user.set_password(password)
        user.save()
        return user




class InsuredSerializers(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=InsuredProfile
        fields='__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Certificate
        fields='__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields='__all__'

class PolicySerializers(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    certificate = CertificateSerializer(many=True,read_only=True)
    payments = PaymentSerializer(many=True,read_only=True)
    
    class Meta:
        model=Policy
        fields='__all__'
        read_only_fields = ('premium', 'is_active', 'policy_number', 'valid_till')

class ProductSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Product
        fields='__all__'
        

class MTPPSerializers(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    certificate = CertificateSerializer(many=True,read_only=True)
    payments = PaymentSerializer(many=True,read_only=True)
    reason = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pol_num = f'MMT-{get_pol_num()}'
        if('duration' in validated_data):
            validated_data.pop('duration')
        policy = MotorThirdPartyPolicy(policy_number=pol_num, in_active_reason=1, duration='Yearly', **validated_data)
        policy.save()
        return policy


    class Meta:
        model=MotorThirdPartyPolicy
        fields='__all__'
        read_only_fields = ('premium', 'is_active', 'policy_number', 'valid_till')


class MCPSerializers(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    certificate = CertificateSerializer(many=True,read_only=True)
    payments = PaymentSerializer(many=True,read_only=True)
    reason = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pol_num = f'MMC-{get_pol_num()}'
        policy = MotorComprehensivePolicy(policy_number=pol_num, in_active_reason=1, **validated_data)
        policy.save()
        return policy


    class Meta:
        model=MotorComprehensivePolicy
        fields='__all__'
        read_only_fields = ('premium', 'rate', 'is_active', 'policy_number', 'valid_till')


class ClaimSerializers(serializers.ModelSerializer):
    #url = serializers.CharField(source='get_absolute_url', read_only=True)
    class Meta:
        model=Policy
        fields='__all__'

class InjuredSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Injured
        exclude=['id', 'claim',]

class NotificationSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=PushNotification
        exclude=['token']


class MotorCliamSerializers(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    injureds = InjuredSerializers(many=True, read_only=True)

    class Meta:
        model=MotorClaim
        fields='__all__'
        

class ItemSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Item
        fields=['item', 'value']

class HomeExtraSerializers(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    items = ItemSerializers(many=True)
    payments = PaymentSerializer(many=True,read_only=True)
    reason = serializers.CharField(read_only=True)

    class Meta:
        model=HomeXtra
        fields='__all__'
        read_only_fields = ('premium', 'is_active', 'policy_number', 'valid_till')


    def validate(self, data):
        
        plans = {'Bronze': 500000, 'Silver': 750000, 'Gold': 1000000}
        plan = data['plan']

        if data['items'] and len(data['items']):

            for item in data['items']:
                if item['item'] == "" or item['value'] == "":
                    raise serializers.ValidationError({"household items": "Item Field or value field can not be blank."})

            total = 0
            for item in data['items']:
                total += float(item['value'])
            
            if plans[plan] < total:
                raise serializers.ValidationError({"household items": "Total amount for contents insured for selected plan exceeded."})

        else:
            raise serializers.ValidationError({"household items": 'No Household Item was provided'})

        return data


    def create(self, validated_data):
        
        
        pol_num = f'MHX-{get_pol_num()}'
        
        items = None

        if 'items' in validated_data:
            items = validated_data.pop('items')

        if('duration' in validated_data):
            validated_data.pop('duration')
        

        home = HomeXtra(policy_number=pol_num, in_active_reason=1, duration='Yearly', **validated_data)
        home.save()
       
        
        for item in items:
            if item['item'] == "" or item['value'] == "":
                continue
            it = Item(policy=home, **item)
            it.save()

        return home


class BranchSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Branch
        fields='__all__'

class VehicleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=VehicleModel
        fields=['make', 'model']

class HistorySerializers(serializers.ModelSerializer):
    
    class Meta:
        model=History
        fields='__all__'