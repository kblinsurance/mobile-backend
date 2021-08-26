from kbl.permissions import IsLoggedInUserOrAdmin
from django.shortcuts import render
from django.core.mail import BadHeaderError, message, send_mail, send_mass_mail
from smtplib import SMTPException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from datetime import datetime
import base64

from kbl.models import User

# Create your views here.


class PasswordReset(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):

        email = request.query_params.get('email')
        if not email:
            return Response(dict(message="Email missing in request"), status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email.lower())
            res = send_mail(
                "Email verification",
                f'Dear {user.first_name}\n\n Please use this link to reset your password.\n\n Ignore this mail if you did not initiate this.\n\n Thank you.',
                'no_reply@kblinsurance.com',
                [user.email],
                fail_silently=False,
            )
            print(res)
            return Response(dict(message="Email has been sent"), status.HTTP_200_OK)
        except BadHeaderError as e:
            return Response(dict(message="Invalid header found"), status.HTTP_500_INTERNAL_SERVER_ERROR)
        except SMTPException as e:
            print(e)
            return Response(dict(message='Something Happened.'), status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactMail(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        if not email or not subject or not message or not name:
            return Response(dict(message="Some fields are missing in request"), status.HTTP_400_BAD_REQUEST)

        try:
            
            res = send_mail(
                subject,
                f'{message}\n\n\rFrom {name}',
                email,
                ['no_reply@kblinsurance.com'],
                fail_silently=False,
            )

            sec = send_mail(
                subject,
                f'Dear {name}\n\nThank you for reaching out to us, our representative will get back to you soon\n\nThank you',
                'no_reply@kblinsurance.com',
                [email],
                fail_silently=False,
            )
            
            return Response(dict(message="Email has been sent"), status.HTTP_200_OK)
        except BadHeaderError as e:
            return Response(dict(message="Invalid header found"), status.HTTP_500_INTERNAL_SERVER_ERROR)
        except SMTPException as e:
            print(e)
            return Response(dict(message='Something Happened.'), status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClaimsMail(APIView):

    permission_classes = [IsLoggedInUserOrAdmin]

    @staticmethod
    def post(request):
        pk = request.data.get('user')
        

        policy = request.data.get('policy')
        details = request.data.get('details')
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not policy:
            return Response(dict(message="Policy number missing in request"), status.HTTP_400_BAD_REQUEST)

        if not details:
            return Response(dict(message="Details of Accident missing in request"), status.HTTP_400_BAD_REQUEST)

        if not pk:
            return Response(dict(message="User missing in request"), status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response(dict(message="Email of Accident missing in request"), status.HTTP_400_BAD_REQUEST)

        if not phone:
            return Response(dict(message="Phone number missing in request"), status.HTTP_400_BAD_REQUEST)


        try:
            user = User.objects.get(pk=pk)
            res = send_mail(
                "Claims Application",
                f'Message Mobile App.\n\n\r{details}\n\n from {user}\n Email: {email}\nPhone: {phone}',
                user.email,
                ['no_reply@kblinsurance.com'],
                fail_silently=False,
            )

            sec = send_mail(
                "Claims Application",
                f'Dear {user}\n\nThank you for reaching out to us, our representative will get back to you soon\n\nThank you',
                'no_reply@kblinsurance.com',
                [user.email],
                fail_silently=False,
            )
            
            return Response(dict(message="Claims submit successfully"), status.HTTP_200_OK)
        except BadHeaderError as e:
            return Response(dict(message="Invalid header found"), status.HTTP_500_INTERNAL_SERVER_ERROR)
        except SMTPException as e:
            print(e)
            return Response(dict(message='Something Happened.'), status.HTTP_500_INTERNAL_SERVER_ERROR)


class PolicyReviewMail(APIView):

    permission_classes = [IsLoggedInUserOrAdmin]

    @staticmethod
    def post(request):
        pk = request.data.get('user')
        

        policy = request.data.get('policy')
        details = request.data.get('details')
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not policy:
            return Response(dict(message="Policy number missing in request"), status.HTTP_400_BAD_REQUEST)

        if not details:
            return Response(dict(message="Details of Accident missing in request"), status.HTTP_400_BAD_REQUEST)

        if not pk:
            return Response(dict(message="User missing in request"), status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response(dict(message="Email of Accident missing in request"), status.HTTP_400_BAD_REQUEST)

        if not phone:
            return Response(dict(message="Phone number missing in request"), status.HTTP_400_BAD_REQUEST)


        try:
            user = User.objects.get(pk=pk)
            res = send_mail(
                "Claims Application",
                f'Message Mobile App.\n\n\r{details}\n\n from {user}\n Email: {email}\nPhone: {phone}',
                user.email,
                ['no_reply@kblinsurance.com'],
                fail_silently=False,
            )

            sec = send_mail(
                "Claims Application",
                f'Dear {user}\n\nThank you for reaching out to us, our representative will get back to you soon\n\nThank you',
                'no_reply@kblinsurance.com',
                [user.email],
                fail_silently=False,
            )
            
            return Response(dict(message="Claims submit successfully"), status.HTTP_200_OK)
        except BadHeaderError as e:
            return Response(dict(message="Invalid header found"), status.HTTP_500_INTERNAL_SERVER_ERROR)
        except SMTPException as e:
            print(e)
            return Response(dict(message='Something Happened.'), status.HTTP_500_INTERNAL_SERVER_ERROR)