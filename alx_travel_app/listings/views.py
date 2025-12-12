from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
import os
import requests
import uuid
import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from .tasks import send_payment_confirmation_email

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response({'error': 'Booking ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        booking = get_object_or_404(Booking, id=booking_id)
        amount = booking.listing.price
        tx_ref = f'chapa-tx-{uuid.uuid4()}'
        chapa_secret_key = os.environ.get('CHAPA_SECRET_KEY')

        headers = {
            'Authorization': f'Bearer {chapa_secret_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'amount': str(amount),
            'currency': 'ETB',
            'email': booking.guest.email,
            'first_name': booking.guest.first_name,
            'last_name': booking.guest.last_name,
            'tx_ref': tx_ref,
            'callback_url': f'http://{request.get_host()}/api/verify-payment/{tx_ref}/',
            'return_url': f'http://{request.get_host()}/payment-success/',
            'customization[title]': 'Payment for Booking',
            'customization[description]': f'Booking ID: {booking.id}'
        }

        try:
            chapa_url = 'https://api.chapa.co/v1/transaction/initialize'
            response = requests.post(chapa_url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status') == 'success':
                Payment.objects.create(
                    booking=booking,
                    amount=amount,
                    transaction_id=tx_ref,
                    payment_status='Pending'
                )
                return Response(response_data)
            else:
                logger.error(f"Chapa API error: {response_data}")
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Chapa API failed: {e}")
            return Response({'error': 'Could not connect to payment gateway'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentView(APIView):
    def get(self, request, tx_ref, *args, **kwargs):
        chapa_secret_key = os.environ.get('CHAPA_SECRET_KEY')
        headers = {
            'Authorization': f'Bearer {chapa_secret_key}',
        }

        try:
            chapa_url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
            response = requests.get(chapa_url, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status') == 'success':
                payment = get_object_or_404(Payment, transaction_id=tx_ref)
                payment.payment_status = 'Completed'
                payment.save()

                # Send confirmation email
                send_payment_confirmation_email.delay(payment.booking.guest.email, payment.booking.id)

                return Response({'message': 'Payment verified successfully'})
            else:
                payment = get_object_or_404(Payment, transaction_id=tx_ref)
                payment.payment_status = 'Failed'
                payment.save()
                logger.error(f"Chapa verification error: {response_data}")
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Chapa API failed: {e}")
            return Response({'error': 'Could not connect to payment gateway'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)