from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db import transaction
from rest_framework.authtoken.models import Token


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
YES_NO_CHOICES = (('Y', 'Yes'), ('N', 'No'),)
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Documents(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()


class Address(models.Model):
    street_name = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)


class InvestmentStrategy(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    smsfund = models.ForeignKey(to='SMSFund', related_name='investment_strategies', on_delete=models.CASCADE)


class SFund(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    smsf_member = models.ForeignKey(to='SMSFMember', related_name='sfunds', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)


class SMSFund(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    documents = models.ManyToManyField(to='Documents')
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)


class Member(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=17, blank=True, null=True)

    class Meta:
        abstract = True


class StaffMember(Member):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True)

    @transaction.atomic
    def create_staff_member(self, username, email, password):
        django_user = User.objects.create_user(username=username, email=email, password=password)
        Token.objects.create(user=django_user)
        staff_member = StaffMember.objects.create(user=django_user)
        staff_member.user = django_user
        staff_member.save()
        return staff_member


class SMSFMember(Member):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True)
    annual_income = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mothers_maiden_name = models.CharField(max_length=20, blank=True, null=True)
    tax_file_number = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer = models.CharField(max_length=20, blank=True, null=True)

    smsfund = models.ForeignKey(to='SMSFund', related_name='smsf_members', null=True, on_delete=models.CASCADE)
    contact_owner = models.ForeignKey(to='StaffMember', blank=True, null=True, on_delete=models.CASCADE)
    documents = models.ManyToManyField(to='Documents')
    place_of_residence = models.OneToOneField(to='Address', related_name='smsf_member_place_of_residence', blank=True, null=True, on_delete=models.CASCADE)
    place_of_birth = models.OneToOneField(to='Address', related_name='smsf_member_place_of_birth', blank=True, null=True,on_delete=models.CASCADE)
    accept_terms = models.CharField(max_length=1, choices=YES_NO_CHOICES, blank=True, null=True)

    @transaction.atomic
    def create_smsf_member(self, **user):
        self.user = User.objects.create_user(**user)
        Token.objects.create(user=self.user)
        self.save()
        return self
