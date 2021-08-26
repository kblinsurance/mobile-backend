from .policy import Policy, History
from .user import *
from .motor import MotorComprehensivePolicy, MotorThirdPartyPolicy
from .payment import PaymentHistory, Payment
from .product import Product, Premium
from .claim import Claim
from .motorClaim import MotorClaim, Injured
from .homeExtra import HomeXtra, Item
from .certificate import Certificate
from .branch import Branch
from .pushnotification import PushNotification, PushNotificationToken
from .vehicles import VehicleModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=MotorComprehensivePolicy)
@receiver(post_save, sender=MotorThirdPartyPolicy)
@receiver(post_save, sender=HomeXtra)
@receiver(post_save, sender=Policy)
def save_history_pol(sender, instance, created,**kwargs):
    
    if created:
        history = History(user=instance.user, type="Policy", desc=f"Policy - {instance.policy_number} was created")
        history.save()


@receiver(post_save, sender=Certificate)
def save_history_cert(sender, instance, created,**kwargs):
    
    if created:
        history = History(user=instance.policy.user , type="Policy", desc=f"Certificate for Policy {instance.policy.policy_number} is now downloadable")
        history.save()