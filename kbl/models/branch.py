from django.db import models
from django.utils.translation import ugettext_lazy as _

class Branch(models.Model):
    region = models.CharField(_("Region"), max_length=50)
    address = models.CharField(_("Address"), max_length=255)
    tel_one = models.CharField(_("Telphone 1"), max_length=15)
    tel_two = models.CharField(_("Telephone 2"), max_length=15, null=True, blank=True)
    last_modified = models.DateField(_("Last Modified"), auto_now=True)

    def __str__(self):
        return f'{self.region} Branch'
    