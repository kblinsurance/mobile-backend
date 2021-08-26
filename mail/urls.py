from mail.views import ContactMail, PasswordReset, ClaimsMail
from django.urls import path

urlpatterns = [
    path("user/reset-password/", PasswordReset.as_view(), name="request password reset"),
    path("contact-us/", ContactMail.as_view(), name="contact us by mail"),
    path("mail/claims/application/", ClaimsMail.as_view(), name="Claims Application")
]
