from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('verify-payment/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
]
