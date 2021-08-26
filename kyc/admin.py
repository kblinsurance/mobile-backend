from django.contrib import admin
from .models import KYC
from django.utils.translation import ugettext_lazy as _
from .utility import export_to_csv
# Register your models here.

export_to_csv.short_description = 'Export to CSV'

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    
    #inlines = [InlineIndividualProfile, InlineCorporateProfile]

    fieldsets = (
        (_('Basic info'), {'fields': ('name', 'email','phone','address','state','policy_number', )}),
        (_('Identification'), {'fields': ('id_type', 'id_number', 'id_image', ('issued_at', 'expired_at'))}),
        (_('Profile type'), {'fields': ('is_individual', 'is_corporate'),}),
        (_('Individual'), {'fields': ('dob', 'gender', 'occupation'),}),
        (_('Corporate'), {'fields': ('tin', 'inc_date', 'rc_number', 'inc_cert', 'website', 'sector')}),
        (_('Signature'), {'fields': ('signature',)}),
        (_('Other Information'), {'fields': ('other',)}),
    )
    
    list_display= ['name', 'email', 'phone', 'address', 
                    'state','occupation', 'policy_number', 'gender', 
                    'sector', 'is_individual', 'is_corporate']

    actions = [export_to_csv]