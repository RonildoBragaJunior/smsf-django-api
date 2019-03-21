from django.contrib.auth.models import User
from rest_framework import serializers

from smsf.models import Documents, SMSFund, SFund, InvestmentStrategy, StaffMember, Address


class StaffMemberSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    def create(self, validated_data):
        username = self.data.pop('username')
        password = self.data.pop('password')

        user = User.objects.create_user(username=username, password=password)
        smsf_member = StaffMember.objects.create(user_profile=user.userprofile)
        return smsf_member


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('__all__')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('__all__')


class InvestmentStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentStrategy
        fields = ('__all__')


class SFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = SFund
        fields = ('__all__')


class SMSFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSFund
        fields = ('__all__')




