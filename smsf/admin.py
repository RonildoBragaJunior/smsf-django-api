from django.contrib import admin

from smsf.models import Documents, SMSFund, SMSFMember, SFund, InvestmentStrategy, Address, StaffMember

admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(SMSFund)
admin.site.register(SMSFMember)
admin.site.register(SFund)
admin.site.register(StaffMember)
admin.site.register(InvestmentStrategy)
