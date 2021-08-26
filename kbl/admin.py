from kbl.models.payment import Payment
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext_lazy as _

# Register your models here.
#from .models import InsuredProfile, Identification, OfficerProfile, InsuredOfficer, User
from .models import *
from .forms import CustomUserCreationForm, ProductAdminForm


class CustomUserAdmin(UserAdmin):
    ''' UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('phone','address', 'town', 'state', 'country',)}),
    )'''
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','phone','address', 'state', 'profile_image','referrer',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Profile type'), {'fields': ('is_individual', 'is_corporate'),}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone'),
        }),
    )

    list_display = ['email','first_name', 'last_name', 'phone','address', 'state', 'is_staff', 'is_active', 'referrer']
    ordering = ['email', 'first_name', 'username', 'last_name']
    search_fields = ('email', 'first_name', 'last_name', 'referrer')

admin.site.register(User, CustomUserAdmin)

class IdentificationInline(admin.TabularInline):
    model = Identification
    extra = 0


class PremiumInline(admin.TabularInline):
    model = Premium
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'on_mobile', 'category', 'purchase_link']
    list_filter = ['on_mobile']
    inlines = [PremiumInline]
    form = ProductAdminForm

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(HomeXtra)
class HomeExtraPolicyAdmin(admin.ModelAdmin):
    inlines=[ItemInline, CertificateInline]
    readonly_fields = ('premium', 'policy_number')
    list_display = ['policy_number', 'get_user', 'plan', 'get_product', 'value', 'premium', 'is_active', 'valid_till', 'get_created_at']

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    inlines=[PaymentInline, CertificateInline]
    readonly_fields = ('premium', 'policy_number')
    list_display = ['policy_number', 'user', 'get_product', 'value', 'premium', 'created_at']


@admin.register(MotorThirdPartyPolicy)
class MotorTPPolicyAdmin(admin.ModelAdmin):
    inlines=[PaymentInline, CertificateInline]
    readonly_fields = ('premium', 'policy_number', 'back_image', 'front_image')
    list_display = ['policy_number', 'registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'get_user', 'get_product', 'value', 'premium', 'duration', 'is_active', 'valid_till', 'get_created_at']

@admin.register(MotorComprehensivePolicy)
class MotorCPolicyAdmin(admin.ModelAdmin):
    inlines=[PaymentInline, CertificateInline]
    readonly_fields = ('premium', 'rate', 'policy_number', 'back_image', 'front_image')
    list_display = ['policy_number', 'registration_number', 'get_user', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'get_product', 'value', 'premium', 'duration', 'rate', 'is_active', 'valid_till', 'get_created_at']

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('ref_num', 'policy', 'platform', 'created_at')
    list_display = ['ref_num', 'policy', 'platform', 'created_at',]

class InjuredInline(admin.TabularInline):
    model = Injured
    extra = 0

@admin.register(MotorClaim)
class MotorClaimsAdmin(admin.ModelAdmin):
    inlines = [InjuredInline]
    readonly_fields = ('claim_number',)

    fieldsets = (
        (None, {'fields': ('user', 'policy')}),
        (_('Basic info'), {'fields': ('accident_date', 'accident_time','accident_place','desc', 'damage_desc','est_cost', 'status')}),
        (_('Driver'), {'fields': ('driver', 'driver_phone', 'driver_licence', 'licence_date_issued', 'licence_date_expired',
                                       'present_in_vehicle', 'current_location')}),
        (_('Third Party'), {'fields': ('cause_by_tp', 'tp_name', 'tp_phone', 'tp_address',),}),
        (_('Others'), {'fields': ('police_report', 'other_policy', 'damage_prop_live')}),
        (_('Sign'), {'fields': ('signature', 'report_date',)}),
        (_('Witness'), {'fields': ('witness_name', 'witness_address', 'witness_signature', 'witness_date')}),
    )

@admin.register(Claim)
class ClaimsAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['region', 'address', 'tel_one', 'tel_two', 'last_modified']

@admin.register(VehicleModel)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'created_at']

@admin.register(PushNotification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'title', 'read', 'body', 'time']