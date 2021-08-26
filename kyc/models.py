from django.db import models
from django.utils.translation import ugettext_lazy as _
from kbl.constants import STATE, ID_TYPES, GENDER,SECTORS
from kbl.models import Identification
# Create your models here.
class KYC(models.Model):
    name = models.CharField(_("Name"), max_length=50, help_text="Individual Fullname (surname First), Corporate (Business name)")
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone = models.CharField(_("Phone"), max_length=14)
    policy_number = models.CharField(_("Policy number"), max_length=50, null=True, blank=True)
    occupation = models.CharField(_("Occupation"), max_length=50, blank=True)
    sector = models.CharField(_("Sector"), max_length=50, help_text="Business Sector", choices=SECTORS, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=254,)
    state = models.CharField(_("State"), max_length=50, choices=STATE)
    id_type = models.CharField(_("Type of ID"), max_length=50, choices=ID_TYPES, )
    id_number = models.CharField(_("ID Number"), max_length=50,)
    id_image = models.ImageField(_("Upload Image"), upload_to="identification",help_text="Upload image of ID")
    issued_at = models.DateField(_("Issued Date"), )
    expired_at = models.DateField(_("Expiry Date"))
    is_corporate = models.BooleanField(_("Corporate organization"), help_text="Select if corporate")
    is_individual = models.BooleanField(_("Individual"), help_text="Select if individual")
    gender = models.CharField(_("Gender"), max_length=50, choices=GENDER, null=True, blank=True)
    dob = models.DateField(_("Date of Birth"), null=True, blank=True)
    website = models.URLField(_("Website"), max_length=254, null=True, blank=True)
    inc_cert = models.ImageField(_("Upload Image"), upload_to="certificate", help_text="Upload image of certificate of incorporation", null=True, blank=True)
    inc_date = models.DateField(_("Incorporation Date"), null=True, blank=True)
    tin = models.BigIntegerField(_("Tax Identification Number"), null=True, blank=True)
    rc_number = models.BigIntegerField(_("Registration Number"), null=True, blank=True)
    signature = models.ImageField(_("Signature"), upload_to="signature", help_text="Upload image of Signature")
    other = models.TextField(_("Other Information"), null=True, blank=True)
    created_at = models.DateField(_("Enrolled Date"), auto_now_add=True,)
    updated_at = models.DateField(_("Last Modified"), auto_now=True, )

    def __str__(self):
        return f'{self.name}'
