from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from django.dispatch import receiver
from .signals import user_signed_up

from django.apps import apps
from django.db import connection
import base64


@shared_task
def hello():
    return "Hello, World!"


@shared_task
def send_confirmation_email(email):
    subject = 'Confirm Your Email'
    message = f'Hi, please confirm your email by clicking on this link: {settings.FRONTEND_BASE_URL}/confirm-email/{email}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


@receiver(user_signed_up)
def on_user_signed_up(sender, email, **kwargs):
    send_confirmation_email.delay(email)


@shared_task
def send_daily_user_signup_email():
    UserModel = apps.get_model('login.Users')
    # Get all users created within the last 24 hours
    today = timezone.now()
    yesterday = today - timezone.timedelta(days=1)
    new_users = UserModel.objects.filter(date_joined__gte=yesterday, date_joined__lt=today)

    # Create the email message
    subject = 'New User Signups for Today'
    message = 'The following users signed up today:\n\n'
    for user in new_users:
        message += f'{user.email}\n'
    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = ['voanhluc258@gmail.com']
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def check_db_health():
    try:
        connection.ensure_connection()
        return 'Nothing Fail In DB'
    except Exception as e:
        subject = 'Database Health Check Failed'
        message = f'The database health check failed with the following error:\n\n{str(e)}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['voanhluc258@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
        return 'Fail In DB'
