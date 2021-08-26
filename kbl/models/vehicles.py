from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime


class VehicleModel(models.Model):

    make = models.CharField(_("Make"), max_length=50)
    model = models.CharField(_("Model"), max_length=50)
    created_at = models.DateTimeField(_("Added"), default=datetime.datetime.now)

    def __str__(self):
        return f'{self.make} {self.model}'
