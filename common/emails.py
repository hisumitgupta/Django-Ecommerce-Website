from email import message
import imp
from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token ):
    subject = 'varifiy Your account'
    email_from = settings.EMAIL_HOST_USER
    message = f'Activate Your account On this link http://localhost:8000/User_account/activate/{email_token}'
    send_mail(subject, message, email_from, [email])















