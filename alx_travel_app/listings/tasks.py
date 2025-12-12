from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    """
    Sends a payment confirmation email to the user.
    """
    send_mail(
        'Payment Confirmation',
        f'Your payment for booking ID {booking_id} has been successfully processed.',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )
