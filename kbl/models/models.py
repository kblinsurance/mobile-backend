from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from datetime import date
import time

from .constants import STATE


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone',]
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    phone = models.CharField( max_length=50, unique=True)
    address = models.CharField(max_length=254, verbose_name="Contact Address", null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE, null=True, blank=True)
    is_corporate = models.BooleanField(_("Corporate organization"), help_text="Select if corporate", null=True)
    is_individual = models.BooleanField(_("Individual"), help_text="Select if individual", null=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class InsuredProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    nationality = models.CharField(max_length=50, null=True, blank=True)
    origin_state = models.CharField(verbose_name="State of Origin", max_length=50, choices=STATE, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    bvn = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    


class Identification(models.Model):
    NIN = 'National ID'
    DL = 'Drivers License'
    INT = 'Int Passport'
    VC = 'Voters card'
    TYPES = [
        (NIN, 'National ID'), (DL, 'Drivers License'),
        (INT, 'Int Passport'), (VC, 'Voters Card')
    ]

    type = models.CharField(max_length=50, choices=TYPES)
    id_number = models.BigIntegerField()
    image = models.ImageField(upload_to="static/identifications/", max_length=100, help_text="upload a clear picture of your ID")
    date_issued = models.DateField()
    expiry_date = models.DateField()
    insured = models.ForeignKey('InsuredProfile', on_delete=models.CASCADE, verbose_name="Valid ID")
    

    def __str__(self):
        return f'ID for {self.insured.user.first_name} {self.insured.user.last_name}'



class OfficerProfile(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="officer")
    branch = models.CharField( max_length=50, null=True, blank=True)

    accounts = models.ManyToManyField(InsuredProfile, 
                                        verbose_name="List of Account under officer",
                                        through='InsuredOfficer',
                                        through_fields=('officer', 'insured')
                                    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class InsuredOfficer(models.Model):
    insured = models.ForeignKey(InsuredProfile, verbose_name="Insured", on_delete=models.CASCADE)
    officer = models.ForeignKey(OfficerProfile, verbose_name="Officer", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.officer.first_name}'

    class Meta:
        ordering = ['officer']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_staff:
		OfficerProfile.objects.get_or_create(user = instance)
	else:
		InsuredProfile.objects.get_or_create(user = instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff:
        OfficerProfile.objects.get_or_create(user = instance)
    else:
        InsuredProfile.objects.get_or_create(user = instance)


class Product(models.Model):

    AVAL = True
    NAVAL = False

    AV = [(AVAL, 'Yes'), (NAVAL, 'No')]

    name = models.CharField(_("Name"), max_length=50)
    description = RichTextField(_("Description"))
    featured_image = models.ImageField(_("Upload Image"), upload_to="products/images", help_text="Product Featured Image", null=True, blank=True)
    mobile_icon = models.ImageField(_("Mobile_icon"), upload_to="products/icons", help_text="Icon Image for mobile app", null=True, blank=True)
    on_mobile = models.BooleanField(_("On mobile?"), choices=AV, help_text='Is it purchasable on the mobile app')
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now=True)

    def __str__(self):
        return f'{self.name}'
    

class Premium(models.Model):
    RATE = 'Rate'
    FIXED = 'Fixed'
    TYPE = [(RATE, 'Rate'), (FIXED, 'fixed')]
    option = models.CharField(_("Option"), max_length=50)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount/Rate"), help_text="Enter rate between 0.0 - 1.0 or Fixed amount")
    type = models.CharField(_("Type"), max_length=50, help_text="Fixed amount or rate", choices=TYPE)
    created_at = models.DateField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now_add=True)

    def __str__(self):
        return f'{self.option} {self.amount}'


def get_pol_num():
    milli_sec = int(round(time.time() * 1000))
    return f'MBPN{milli_sec}'

class Policy(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    policy_number = models.CharField(_("Policy Number"), max_length=255, default=get_pol_num)
    premium = models.FloatField(_("Premium"), help_text="Leave blank! Auto calculated on save.")
    value = models.FloatField(_("Value"), help_text="market cost of item")
    front_image = models.ImageField(_("Front Image"), upload_to="policy", max_length=255, help_text="Front image of property")
    back_image = models.ImageField(_("Back Image"), upload_to="policy", max_length=255, help_text="Back image of property")
    certificate = models.URLField(_("Certificate"), max_length=255, null=True, blank=True, help_text="Downloadable as PDF")
    valid_till = models.DateField(_("Valid Till"))
    is_active = models.BooleanField(_("Active"), default=False)
    created_at = models.DateField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Policy -- {self.policy_number}'

    


class MotorThirdPartyPolicy(Policy):
    class Meta:
        verbose_name_plural = "Motor Third-Party polices"
    CLASSES = [
        ('Commercial', 'Commercial'),('Company, Taxi, Car Hire', 'Company, Taxi, Car Hire'),
        ('Stage Carriage 8 - 15 persons', 'Stage Carriage 8 - 15 persons'),
        ('Stage Carriage over 15 persons', 'Stage Carriage over 15 persons'),
        ('Buses, Omnibus', 'Buses, Omnibus'),('Motorcycle/Tricycle', 'Motorcycle/Tricycle'),
        ('Tractor & Equipment', 'Tractor & Equipment'), ('Private Vehicle / Car', 'Private Vehicle / Car'),
    ]
    registration_number = models.CharField(_("Registration Number"), max_length=50)
    engine_number = models.CharField(_("Engine Number"), max_length=50)
    chasis_number = models.CharField(_("Chasis Number"), max_length=50)
    vehicle_class = models.CharField(_("Vehicle Class"), max_length=50, choices=CLASSES)
    vehicle_model = models.CharField(_("Vehicle Model"), max_length=50, help_text="Format vehicle_name vehicle_model (year)")
    vehicle_license = models.ImageField(_("Vehicle License"), upload_to="licenses", max_length=255)
    proof_of_ownership = models.ImageField(_("Proof of ownership"), upload_to="pow", max_length=255)

    def __str__(self):
        return f'{self.vehicle_model} with reg no. {self.registration_number}'

@receiver(pre_save, sender=MotorThirdPartyPolicy)
def calc_third_party_premium(sender, instance, **kwargs):
    if instance.premium != 5000:
        instance.premium = 5000
		
class MotorComprehensivePolicy(Policy):
    class Meta:
        verbose_name_plural = "Motor Comprehensive polices"
    CLASSES = [
        ('Commercial', 'Commercial'),('Company, Taxi, Car Hire', 'Company, Taxi, Car Hire'),
        ('Stage Carriage 8 - 15 persons', 'Stage Carriage 8 - 15 persons'),
        ('Stage Carriage over 15 persons', 'Stage Carriage over 15 persons'),
        ('Buses, Omnibus', 'Buses, Omnibus'),('Motorcycle/Tricycle', 'Motorcycle/Tricycle'),
        ('Tractor & Equipment', 'Tractor & Equipment'), ('Private Vehicle / Car', 'Private Vehicle / Car'),
    ]
    rate = models.FloatField(_("Rate"), help_text="Rate applied on Item Value")
    registration_number = models.CharField(_("Registration Number"), max_length=50)
    engine_number = models.CharField(_("Engine Number"), max_length=50)
    chasis_number = models.CharField(_("Chasis Number"), max_length=50)
    vehicle_class = models.CharField(_("Vehicle Class"), max_length=50, choices=CLASSES)
    vehicle_model = models.CharField(_("Vehicle Model"), max_length=50, help_text="Format vehicle_name vehicle_model (year)")
    vehicle_license = models.ImageField(_("Vehicle License"), upload_to="licenses", max_length=255)
    proof_of_ownership = models.ImageField(_("Proof of ownership"), upload_to="pow", max_length=255)

    def __str__(self):
        return f'{self.vehicle_model} with reg no. {self.registration_number}'


@receiver(pre_save, sender=MotorComprehensivePolicy)
def calc_comp_premium(sender, instance, **kwargs):

    value = instance.value

    if value >= 5000000:
        instance.premium = 0.025 * value
        instance.rate = 0.025
    else:
        instance.premium = 0.03 * value
        instance.rate = 0.03
        
    
class PaymentHistory(models.Model):
    PLT = [('Flutterwave', 'Flutterwave'), ('QuickTeller', 'QuickTeller')]
    policy = models.CharField(verbose_name=_("Policy"), max_length=255)
    ref_num = models.CharField(_("Reference Code"), max_length=255)
    platform = models.CharField(_("Payment Gateway"), max_length=255, choices=PLT)
    created_at = models.DateTimeField(_("Time of Payment"), auto_now=True)

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f'Payment detail for Policy: {self.policy}'
    
@receiver(post_save, sender=PaymentHistory)
def update_policy_status(sender, instance, created, **kwargs):
    policy = Policy.objects.get(policy_number=instance.policy)
    if policy:
        policy.is_active = True