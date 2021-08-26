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
from .policy import Policy
from kbl.constants import BUILDING, PLAN


class HomeXtra(Policy):
    plan = models.CharField(_("Plan"), max_length=50, choices=PLAN, default='Gold')
    building_type = models.CharField(_("Type of Building"), max_length=50, choices=BUILDING, default='Detached Duplex')
    address = models.CharField(_("Address"), max_length=255,)

    def __str__(self):
        return f'Policy for {self.address}'

    def get_user(self):
        return f'{self.user.first_name} {self.user.last_name}'

    get_user.short_description = 'Insured'

    def get_absolute_url(self):
        return f'policies/home-xtra/{self.id}'


@receiver(pre_save, sender=HomeXtra)
def calc_comp_premium(sender, instance, **kwargs):

    plan = instance.plan

    if  plan == 'Bronze':
        instance.premium = 10000
    elif plan == 'Silver':
        instance.premium = 15000
    elif plan == 'Gold':
        instance.premium = 20000


class Item(models.Model):
    policy = models.ForeignKey(HomeXtra, verbose_name=_("Policy"), on_delete=models.CASCADE, related_name='items')
    item = models.CharField(_("Item"), max_length=255,)
    value = models.FloatField(_("Value"))