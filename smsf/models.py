from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Documents(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()


class Address(models.Model):
    street_name = models.CharField(max_length=20)


class InvestmentStrategy(models.Model):
    name = models.CharField(max_length=20, unique=True)
    smsf_fund = models.ForeignKey(to='SMSFund', on_delete=models.CASCADE)


class SFund(models.Model):
    name = models.CharField(max_length=20, unique=True)
    smsf_member = models.ForeignKey(to='SMSFMember', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)


class SMSFund(models.Model):
    name = models.CharField(max_length=20, unique=True)
    documents = models.ManyToManyField(to='Documents')
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Token.objects.create(user=instance)
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class StaffMember(models.Model):
    user_profile = models.OneToOneField(to='UserProfile', on_delete=models.CASCADE)


class SMSFMember(models.Model):
    user_profile = models.OneToOneField(to='UserProfile', on_delete=models.CASCADE)
    smsf_fund = models.ForeignKey(to='SMSFund', null=True, on_delete=models.CASCADE)
    contact_owner = models.ForeignKey(to='StaffMember', blank=True, null=True, on_delete=models.CASCADE)
    Address = models.ForeignKey(to='Address', blank=True, null=True, on_delete=models.CASCADE)
    documents = models.ManyToManyField(to='Documents')

    birth_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=17, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    annual_income = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mothers_maiden_name = models.CharField(max_length=20, unique=True)
    tax_file_number = models.CharField(max_length=20, unique=True)


