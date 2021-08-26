from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from datetime import date
import time
from datetime import timedelta
from django.utils import timezone
from .user import User
from .claim import Claim



class MotorClaim(Claim):

    driver = models.CharField(_("Driver"), max_length=50, help_text="Person Driving at the time of accident")
    driver_phone = models.CharField(_("Driver's Phone"), max_length=15)
    driver_licence = models.CharField(_("Driver's Licence"), max_length=50, help_text="Licence Number")
    licence_date_issued = models.DateField(_("Date Issed"),)
    licence_date_expired = models.DateField(_("Expiry Date"),)
    present_in_vehicle = models.BooleanField(_("Were you in the vehicle?"))
    current_location = models.CharField(_("Location of vehicle"), max_length=50, help_text="Where can we inspect the vehicle?")
    cause_by_tp = models.BooleanField(_("Caused By Third Party?"))
    tp_name = models.CharField(_("Name"), max_length=50)
    tp_phone = models.CharField(_("Phone"), max_length=15)
    tp_address = models.CharField(_("Address"), max_length=255)
    damage_prop_live = models.TextField(_("Damaged Livestock/Property"))
    


    class Meta:
        abstract = False
        verbose_name_plural = 'Motor Claims'

    def __str__(self):
        return f'Claim -- {self.claim_number}'

    def get_absolute_url(self):
        return f'claims/motor/{self.claim_number}'

    
class Injured(models.Model):
    claim = models.ForeignKey(MotorClaim, verbose_name=_("Claim"), on_delete=models.CASCADE, related_name="injureds")
    name = models.CharField(_("Name"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=15, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=255)
    injury = models.CharField(_("Nature of injuries"), max_length=255)
    is_passenger = models.CharField(_("Passenger"), max_length=255)
    in_hospital = models.CharField(_("In Hospital"), max_length=255, null=True, blank=True)
    hospital_detail = models.CharField(_("Hostipal Details"), max_length=1025, null=True, blank=True)

    def __str__(self):
        return f'Registered Injured -- claim {self.claim.claim_number}'

    