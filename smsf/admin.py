from django.contrib import admin

from django.contrib.auth.models import User
from smsf.models import Documents, SMSFund, SMSFMember, SFund, InvestmentStrategy, Address, StaffMember

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']

class SMSFMemberAdmin(admin.ModelAdmin):
    search_fields = ['mobile_number', 'tax_file_number']
    list_display = ('user_email', 'mobile_number', 'tax_file_number',)
    list_filter = ('gender', 'contact_owner','occupation', 'accept_terms')

class SMSFundAdmin(admin.ModelAdmin):
    search_fields = ['name', 'balance']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SMSFMember, SMSFMemberAdmin)
admin.site.register(SMSFund, SMSFundAdmin)
admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(SFund)
admin.site.register(StaffMember)
admin.site.register(InvestmentStrategy)

