from rest_framework import serializers
from kbl.models import MotorThirdPartyPolicy, MotorComprehensivePolicy
from kbl.models.policy import get_pol_num

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

