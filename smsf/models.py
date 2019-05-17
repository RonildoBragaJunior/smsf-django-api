import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.authtoken.models import Token

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
YES_NO_CHOICES = (('Y', 'Yes'), ('N', 'No'),)
ROLLOVER_CHOICES = (('F', 'Full'), ('P', 'Partial'),)
STAFF_ROLE = (('S', 'Sale'), ('O', 'Operations'),('A','Accounting'))
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
SMSF_MEMBER_LEAD_STATUS = (
    ('1', 'New lead'),
    ('2', 'Contact attempted'),
    ('3', 'In progress'),
    ('4', 'Converted'),
    ('5', 'Abandoned')
)


class Documents(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)


class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    street_name = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.street_name)


class InvestmentStrategy(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)


class SFund(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    smsf_member = models.ForeignKey(to='SMSFMember', related_name='sfunds', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    rollover = models.CharField(max_length=1, choices=ROLLOVER_CHOICES, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)


class SMSFund(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    documents = models.ManyToManyField(to='Documents')
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    investment_strategies = models.ManyToManyField(to='InvestmentStrategy', related_name='smsfunds')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name)


class Member(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=17, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def create_user(self, **user):
        self.user = User.objects.create_user(**user)
        Token.objects.create(user=self.user)
        return self


class StaffMember(Member):
    role = models.CharField(max_length=1, choices=STAFF_ROLE, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.user.email)


class SMSFMember(Member):
    smsfund = models.ForeignKey(to='SMSFund', related_name='smsf_members', null=True, blank=True, on_delete=models.CASCADE)
    contact_owner = models.ForeignKey(to='StaffMember', null=True, blank=True, on_delete=models.CASCADE)
    documents = models.ManyToManyField(to='Documents', related_name='documents')
    place_of_residence = models.OneToOneField(to='Address', related_name='smsf_member_place_of_residence', null=True, blank=True, on_delete=models.CASCADE)
    place_of_birth = models.OneToOneField(to='Address', related_name='smsf_member_place_of_birth', null=True, blank=True, on_delete=models.CASCADE)

    annual_income = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    mothers_maiden_name = models.CharField(max_length=20, blank=True, null=True)
    tax_file_number = models.CharField(max_length=40, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer = models.CharField(max_length=20, blank=True, null=True)
    lead_status = models.CharField(max_length=1, choices=SMSF_MEMBER_LEAD_STATUS, default='1')
    accept_terms = models.CharField(max_length=1, choices=YES_NO_CHOICES, blank=True, null=True)
    accept_terms_timestamp = models.DateTimeField(blank=True, null=True)

    @property
    def user_email(self):
        return self.user.email

    def __str__(self):
        return "%s" % (self.user.email)
