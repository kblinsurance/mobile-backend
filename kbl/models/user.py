from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


from kbl.constants import STATE


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
    profile_image = models.ImageField(_("Profile Image"), upload_to="profile", null=True, blank=True)
    referrer = models.CharField(_("Referrer"), max_length=50, null=True, blank=True)
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



    