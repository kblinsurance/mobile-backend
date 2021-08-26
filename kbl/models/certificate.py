from django.core.files import File as DjangoFile
from django.core.mail import BadHeaderError, EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from .policy import Policy
import os
from core.settings import STATIC_ROOT
from django.template.loader import get_template
from xhtml2pdf import pisa
from smtplib import SMTPException
import tempfile
from wkhtmltopdf.views import PDFTemplateResponse

class Certificate(models.Model):
    policy = models.ForeignKey(Policy, verbose_name=_("Policy"), on_delete=models.CASCADE, related_name="certificate")
    certificate = models.FileField(_("Certificate"), upload_to="certificate", storage=RawMediaCloudinaryStorage(), help_text="Downloadable as PDF")
    date = models.DateField(_("Issued Date"), auto_now_add=True)

    def __str__(self):
        return f'Certificate for Policy - {self.policy.policy_number}'
    


def generate_motor_certificate(policy, product):
    pol = None
    if product.category == "Motor":
        pol = policy.motorcomprehensivepolicy if product.name == 'Motor Comprehensive' else policy.motorthirdpartypolicy
    else:
        pol = policy.homextra

    context = {"user": policy.user, 'policy': pol, 'product': product}
    
    template = 'motor_certificate.html' if product.category == "Motor" else 'home_certificate.html'


    fd, path = tempfile.mkstemp()
    file = None

    try:
        response = PDFTemplateResponse(request=None, template=template,
            context=context,
            filename=f'{policy.policy_number}_certificate.pdf',
            cmd_options={'load-error-handling': 'ignore'}
        )
        
        with open(path, "wb") as f:
            f.write(response.rendered_content)

        
        file = DjangoFile(open(path,mode='rb'),name=f'{policy.policy_number}_certificate.pdf')
        
        certificate = Certificate(policy=policy,certificate=file)
        certificate.save()
        
        email = EmailMessage(
            subject="New Policy",
            to=[policy.user.email],
            body=f'Dear {policy.user.first_name} {policy.user.last_name}\n\n Thank you for choosing to insure with KBL Insurance Limited\n\r\n\r\t Your policy number is {policy.policy_number}.\n\n\r Download attached certificate\n\r\n\r  Thank you.\nKBL Insurance Team',
            attachments=[(f'{policy.policy_number}_certificate.pdf',response.rendered_content,'application/pdf')]
        )
        email.send(fail_silently=False)
        
    except BadHeaderError as e:
        print(e)
        print('badHeader')
    except SMTPException as e:
        print(e)
        print('smtp error')
    finally:
        os.remove(path)


    
    
        