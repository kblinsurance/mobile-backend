from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushResponseError,
    PushServerError,
) 
from requests.exceptions import ConnectionError, HTTPError
import datetime
from retry.api import retry_call

from kbl.models import User


class PushNotificationToken(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="token")
    token = models.CharField(_("Push Token"), max_length=255, null=True, blank=True)
    active = models.BooleanField(_("Active"),default=False)
    time = models.DateTimeField(_("Last Modified"),default=datetime.datetime.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.token}'


class PushNotification(models.Model):
    """Push Notification"""
    token = models.ForeignKey(PushNotificationToken, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    body = models.TextField(_("Body"))
    data = models.TextField(_("Data"))
    user = models.ForeignKey(User, verbose_name=_("User"),null=True, blank=True, on_delete=models.CASCADE)
    read = models.BooleanField(_("Read?"), default=False)
    time = models.DateTimeField(_("Time Sent"), default=datetime.datetime.now)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Notifications'


class Expo(ConnectionError):
    
    def retry(self, exc):
        retry_call(exc)


    # Basic arguments. You should extend this function with the push features you
    # want to use, or simply pass in a `PushMessage` object.
    def send_push_message(self, token, title, message, extra=None):
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            title=title,
                            body=message,
                            data=extra,
                            sound='default',
                            badge=2))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            '''rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'errors': exc.errors,
                    'response_data': exc.response_data,
                })'''
            raise
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            #rollbar.report_exc_info(
            #    extra_data={'token': token, 'message': message, 'extra': extra})
            raise #self.retry(exc=exc)

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            
            PushNotificationToken.objects.filter(token=token).update(active=False)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            '''rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'push_response': exc.push_response._asdict(),
                })'''
            #raise self.retry(exc=exc)
            print(exc)


@receiver(post_save, sender=PushNotification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        print("Sending notifications")
        expo = Expo()
        expo.send_push_message(token=instance.token.token,title=instance.title, message=instance.body, extra=instance.data)