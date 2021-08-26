from kbl.constants import DURATION
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .user import User
from .product import Product


class PolicyCount(models.Model):
    count = models.IntegerField(_("Count"), default=000000)

    def __str__(self):
        return f'{self.count}'
    

def get_pol_num():
    try:
        pol_num = PolicyCount.objects.get(id=1)
        pol_num.count += 1
        pol_num.save()
    except ObjectDoesNotExist as e:
        pol_num = PolicyCount()
        pol_num.save()
        pol_num.count += 1
        pol_num.save()
    
    return f'{str(pol_num.count).zfill(6)}KBL'

def return_date_time():
    now = timezone.now()
    return now + timedelta(days=365)

class Policy(models.Model):
    REASONS = [
        (1, 'In complete purchase'),
        (2, 'Under Review'),
        (3, 'Policy has expired')
    ]
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    policy_number = models.CharField(_("Policy Number"), max_length=255, default=get_pol_num)
    premium = models.FloatField(_("Premium"), help_text="Leave blank! Auto calculated on save.")
    product = models.ForeignKey(Product, verbose_name=_("Product"), null=True, on_delete=models.PROTECT)
    value = models.FloatField(_("Value"), help_text="market cost of item", null=True)
    front_image = models.ImageField(_("Front Image"), upload_to="policy", max_length=255, help_text="Front image of property", null=True, blank=True)
    back_image = models.ImageField(_("Back Image"), upload_to="policy", max_length=255, help_text="Back image of property", null=True, blank=True)
    duration = models.CharField(_("Duration"), max_length=50, choices=DURATION, default='Yearly')
    valid_till = models.DateTimeField(_("Valid Till"), null=True)
    is_active = models.BooleanField(_("Active"), default=False)
    in_active_reason = models.CharField(_("Why In Active"), max_length=255, choices=REASONS, null=True, blank=True)
    referrer = models.CharField(_("Referrer"), max_length=50, blank=True, null=True)
    created_at = models.DateField(_("Created At"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Last Modified"), auto_now=True)
    
    class Meta:
        abstract = False
        verbose_name_plural = 'All Policies'
        ordering=['-is_active', '-last_modified']

    def __str__(self):
        return f'Policy -- {self.policy_number}'

    def get_created_at(self):
        return f'{self.created_at}'

    get_created_at.short_description = 'Purchase Date'

    def get_product(self):
        return self.product.name if self.product else "Not Set/Deleted"

    get_product.short_description = 'Product'

    @property
    def reason(self):
        if self.in_active_reason and int(self.in_active_reason) == 1:
            return 'In complete purchase'
        elif self.in_active_reason and int(self.in_active_reason) == 2:
            return 'Under Review'
        elif self.in_active_reason and int(self.in_active_reason) == 3:
            return 'Policy has expired'
        else:
            return ""
            


class History(models.Model):
    CHOICE = [('Policy', 'Policy'), ('Claims', 'Claims')]
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    type = models.CharField(_("Type"), max_length=50, choices=CHOICE)
    desc = models.CharField(_("Description"), max_length=255)
    when = models.DateTimeField(_("When"), auto_now_add=True)

    def __str__(self):
        return f'{self.desc}'

    class Meta:
        ordering = ['-when']
