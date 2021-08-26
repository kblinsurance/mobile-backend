from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver


from .policy import Policy

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
    vehicle_model = models.CharField(_("Vehicle Model"), max_length=50)
    vehicle_make = models.CharField(_("Vehicle Make"), max_length=50,)
    vehicle_year = models.CharField(_("Vehicle Year"), max_length=50)
    vehicle_color = models.CharField(_("Vehicle Color"), max_length=50)
    vehicle_license = models.ImageField(_("Vehicle License"), upload_to="licenses", max_length=255, null=True, blank=True)
    proof_of_ownership = models.ImageField(_("Proof of ownership"), upload_to="pow", max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f'{self.vehicle_model} with reg no. {self.registration_number}'

    def get_user(self):
        return f'{self.user.first_name} {self.user.last_name}'

    get_user.short_description = 'Insured'

    def get_absolute_url(self):
        return f'policies/motor-third-party/{self.id}'

    

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
    vehicle_model = models.CharField(_("Vehicle Model"), max_length=50)
    vehicle_make = models.CharField(_("Vehicle Make"), max_length=50,)
    vehicle_year = models.CharField(_("Vehicle Year"), max_length=50)
    vehicle_color = models.CharField(_("Vehicle Color"), max_length=50)
    vehicle_license = models.ImageField(_("Vehicle License"), upload_to="licenses", max_length=255, null=True, blank=True)
    proof_of_ownership = models.ImageField(_("Proof of ownership"), upload_to="pow", max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f'{self.vehicle_model} with reg no. {self.registration_number}'

    def get_user(self):
        return f'{self.user.first_name} {self.user.last_name}'

    get_user.short_description = 'Insured'

    def get_absolute_url(self):
        return f'policies/motor-comprehensive/{self.id}'



@receiver(pre_save, sender=MotorComprehensivePolicy)
def calc_comp_premium(sender, instance, **kwargs):

    value = instance.value

    if value >= 5000000:
        instance.premium = 0.025 * value
        instance.rate = 0.025
    else:
        instance.premium = 0.03 * value
        instance.rate = 0.03
        