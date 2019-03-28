from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from smsf.models import Documents, SMSFund, SFund, InvestmentStrategy, StaffMember, Address, SMSFMember


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class DocumentsSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField(allow_blank=True, required=False)
    url = serializers.URLField(required=False)

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
    uuid = serializers.CharField(allow_blank=True, required=False)
    balance = serializers.DecimalField(max_digits=64, decimal_places=2, required=False)
    name = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = SFund
        fields = ('uuid', 'name', 'balance')


class SMSFundSerializer(serializers.ModelSerializer):
    investment_strategies = InvestmentStrategySerializer(many=True)
    documents = DocumentsSerializer(many=True, required=False)

    class Meta:
        model = SMSFund
        fields = ('__all__')


class StaffMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', allow_blank=True, required=False)
    email = serializers.CharField(source='user.email', allow_blank=True, required=False)
    password = serializers.CharField(source='user.password', allow_blank=True, required=False)

    class Meta:
        model = StaffMember
        fields = ('__all__')


class SMSFMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', allow_blank=True, required=False)
    email = serializers.CharField(source='user.email', allow_blank=True, required=False)
    password = serializers.CharField(source='user.password', allow_blank=True, required=False)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)

    sfunds = SFundSerializer(many=True, required=False)
    smsfund = SMSFundSerializer(required=False)
    place_of_residence = AddressSerializer(required=False)
    place_of_birth = AddressSerializer(required=False)
    documents = DocumentsSerializer(many=True, required=False)

    class Meta:
        model = SMSFMember
        fields = ('__all__')

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.pop('user')

        if validated_data.get('sfunds') is not None:
            sfunds = validated_data.pop('sfunds')

        if validated_data.get('smsfund') is not None:
            smsfund = validated_data.pop('smsfund')

        if validated_data.get('place_of_residence') is not None:
            place_of_residence = validated_data.pop('place_of_residence')

        if validated_data.get('place_of_birth') is not None:
            place_of_birth = validated_data.pop('place_of_birth')

        smsf_member = SMSFMember(**validated_data).create_user(**user)
        smsf_member.save()

        for sfund in sfunds:
            SFund.objects.create(smsf_member=smsf_member, **sfund)

        return smsf_member

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('user') is not None:
            user = validated_data.pop('user')

        if validated_data.get('sfunds') is not None:
            sfunds = validated_data.pop('sfunds')
            for sfund in sfunds:
                SFund.objects.get_or_create(smsf_member=instance, **sfund)

        if validated_data.get('smsfund') is not None:
            smsfund = validated_data.pop('smsfund')
            if smsfund.get('investment_strategies') is not None:
                investment_strategies = smsfund.pop('investment_strategies')

            smsfund, created = SMSFund.objects.get_or_create(**smsfund)

            if investment_strategies is not None:
                for investment_strategy in investment_strategies:
                    investment_strategy, created = InvestmentStrategy.objects.get_or_create(name=investment_strategy['name'])
                    smsfund.investment_strategies.add(investment_strategy)

            smsfund.save()
            instance.smsfund = smsfund

        if validated_data.get('place_of_residence') is not None:
            place_of_residence = validated_data.pop('place_of_residence')
            place_of_residence, created = Address.objects.get_or_create(smsf_member_place_of_residence=instance, **place_of_residence)
            instance.place_of_residence = place_of_residence

        if validated_data.get('place_of_birth') is not None:
            place_of_birth = validated_data.pop('place_of_birth')
            place_of_birth, created = Address.objects.get_or_create(smsf_member_place_of_birth=instance, **place_of_birth)
            instance.place_of_birth = place_of_birth

        if validated_data.get('annual_income') is not None:
            instance.annual_income = validated_data.pop('annual_income')

        if validated_data.get('mothers_maiden_name') is not None:
            instance.mothers_maiden_name = validated_data.pop('mothers_maiden_name')

        if validated_data.get('tax_file_number') is not None:
            instance.tax_file_number = validated_data.pop('tax_file_number')

        if validated_data.get('occupation') is not None:
            instance.occupation = validated_data.pop('occupation')

        if validated_data.get('employer') is not None:
            instance.employer = validated_data.pop('employer')

        if validated_data.get('accept_terms') is not None:
            instance.accept_terms = validated_data.pop('accept_terms')

        if validated_data.get('gender') is not None:
            instance.gender = validated_data.pop('gender')

        if validated_data.get('birth_date') is not None:
            instance.birth_date = validated_data.pop('birth_date')

        if validated_data.get('mobile_number') is not None:
            instance.mobile_number = validated_data.pop('mobile_number')

        instance.save()
        return instance