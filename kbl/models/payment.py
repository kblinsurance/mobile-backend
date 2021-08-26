from kbl.models.product import Product
from kbl.models.certificate import generate_motor_certificate
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, datetime
from django.core.mail import BadHeaderError, message, send_mail, send_mass_mail
from smtplib import SMTPException
from django.utils import timezone

from .policy import Policy

def return_date_time(duration):
    if duration == 'Quarterly':
        now = timezone.now()
        return now + timedelta(days=91.25)

    elif duration == 'Half Yearly':
        now = timezone.now()
        return now + timedelta(days=182.5)

    elif duration == 'Yearly':
        now = timezone.now()
        return now + timedelta(days=365)

class PaymentHistory(models.Model):
    PLT = [('Flutterwave', 'Flutterwave'), ('QuickTeller', 'QuickTeller')]
    policy = models.CharField(verbose_name=_("Policy"), max_length=255)
    ref_num = models.CharField(_("Reference Code"), max_length=255)
    platform = models.CharField(_("Payment Gateway"), max_length=255, choices=PLT)
    created_at = models.DateTimeField(_("Time of Payment"), auto_now_add=True)

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f'Payment detail for Policy: {self.policy}'

class Payment(models.Model):
    QUARTERLY = "25"
    HALF = '50'
    YEARLY = '100'
    PERC = [('Quarterly',QUARTERLY), ('Half', HALF), ('Yearly', YEARLY)]

    policy = models.ForeignKey(Policy, verbose_name=_("Policy"), on_delete=models.CASCADE, related_name="payments")
    amount = models.FloatField(_("Amount"))
    percentage = models.CharField(_("Percentage"), max_length=50, default='Yearly', choices=PERC)
    start = models.DateTimeField(_("Start Date"),  default=datetime.now)
    end = models.DateTimeField(_("End Date"), null=True)

@receiver(post_save, sender=PaymentHistory)
def update_policy_status(sender, instance, created, **kwargs):
    if created:
        try:
            policy = Policy.objects.get(policy_number=instance.policy)
            duration = policy.duration

            
            policy.is_active = True
            policy.valid_till = return_date_time(duration)
            policy.save()

            amount = 0
            
            if duration == 'Quarterly':
                amount = float(policy.premium) * 0.25
            elif duration == 'Half Yearly':
                amount = float(policy.premium) * 0.5
            elif duration == 'Yearly':
                amount = float(policy.premium)

            payment = Payment(policy=policy, amount=amount, percentage=duration)
            payment.end = return_date_time(duration)
            payment.save()

            product = Product.objects.get(id=policy.product.id)

            if product.name == 'Motor Comprehensive':
                policy.is_active = False
                policy.in_active_reason = 2
                policy.save()
                res = send_mail(
                            "Policy Review",
                            f'Dear Team,\n\r\n\rNew policy with policy-number {policy.policy_number} pending review.\n\rCustomer Details\n\tName: {policy.user.first_name} {policy.user.last_name}\n\tEmail:  {policy.user.email}\n\tPhone: {policy.user.phone}\n\n Thank you.\nKBL Insurance Team',
                            'no_reply@kblinsurance.com',
                            ['KBLInsuranceIT@keystonebankng.com'],
                            fail_silently=False,
                        )
                
                res2 = send_mail(
                            "Policy Review",
                            f'Dear {policy.user.first_name} {policy.user.first_name}, \n\n\rThank you for choosing to insure with KBL Insurance.\n\r\n\rThis is to inform you that your policy is under review and would be made active within the next 24hrs.\n\r\n\rWe value your patronage.\n\r\n Yours faithfully,\nKBL Insurance Team',
                            'no_reply@kblinsurance.com',
                            [policy.user.email],
                            fail_silently=False,
                        )
                return

            policy.in_active_reason = None
            generate_motor_certificate(policy,product)
        except BadHeaderError as e:
            print(e)
            return
        except SMTPException as e:
            print(e)
            return 
        except Exception as e:
            print(e)
