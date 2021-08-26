from kbl.constants import PRODUCTS
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from datetime import date
import time


class Product(models.Model):

    AVAL = True
    NAVAL = False
    MOTOR = 'Motor'
    HOME = 'Home'

    AV = [(AVAL, 'Yes'), (NAVAL, 'No')]
    CATEGORY = [(MOTOR, MOTOR), (HOME,HOME)]

    name = models.CharField(_("Name"), max_length=255, choices=PRODUCTS)
    description = RichTextField(_("Description"))
    featured_image = models.ImageField(_("Upload Image"), upload_to="products/images", help_text="Product Featured Image", null=True, blank=True)
    mobile_icon = models.ImageField(_("Mobile_icon"), upload_to="products/icons", help_text="Icon Image for mobile app", null=True, blank=True)
    on_mobile = models.BooleanField(_("On mobile?"), choices=AV, help_text='Is it purchasable on the mobile app')
    purchase_link = models.CharField(_("Link"), max_length=50, null=True, blank=True, help_text="link to purchase policy")
    category = models.CharField(_("Category"), max_length=50, help_text='Product Category', default='Home', choices=CATEGORY)
    icon = models.CharField(_("Mobile Icon"), max_length=50, null=True, blank=True)
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