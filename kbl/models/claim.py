from kbl.constants import STATUS
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import date
import time
from .user import User
from .policy import Policy

def get_clm_num():
    milli_sec = int(round(time.time() * 1000))
    return f'MBCN-{milli_sec}'


class Claim(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    policy = models.ForeignKey(Policy, verbose_name=_("Policy"), null=True, on_delete=models.SET_NULL)
    claim_number = models.CharField(_("Claim Number"), max_length=50, default=get_clm_num)
    accident_date = models.DateField(_("Date of Accident/loss"),)
    accident_time = models.TimeField(_("Time of Accident/loss"))
    accident_place = models.CharField(_("Place of Accident/loss"), max_length=255, null=True, blank=True)
    desc = models.TextField(_("Description"), help_text="Please describe how the loss occurred")
    damage_desc = models.TextField(_("Damage Description"), null=True, blank=True, help_text="Describe extent of direct damage resulting from the accident")
    est_cost = models.FloatField(_("Estimate"), help_text="Estimated cost of repair")
    police_report = models.TextField(_("Policy Report"), blank=True, null=True)
    other_policy = models.TextField(_("Other Insurance"), help_text="Please give details of any other insurance cover on the vehicle", blank=True, null=True)
    witness_name = models.CharField(_("Witness Name"), max_length=255)
    witness_address = models.CharField(_("Witness Address"), max_length=255)
    witness_signature = models.ImageField(_("Witness Signature"), upload_to="signature", help_text="Upload image of Signature")
    witness_date = models.DateField(_("Date"), default=date.today)
    status = models.CharField(_("Status"), max_length=50, choices=STATUS, default='Processing')
    created_at = models.DateField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now=True)

    
    class Meta:
        abstract = False
        verbose_name_plural = 'Claims'

    def __str__(self):
        return f'Claim -- {self.claim_number}'

    def get_created_at(self):
        return f'{self.created_at}'

    get_created_at.short_description = 'Filed Date'

    def get_policy(self):
        return self.policy.policy_number if self.policy else "Not Set/Deleted"

    get_policy.short_description = 'Policy'

    