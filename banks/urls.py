from django.urls import path

from banks.views import BankListAPIView, BankDetailAPIView


app_name = "banks"

urlpatterns = [
    path("", BankListAPIView.as_view(), name="bank-list"),
    path("<int:pk>/", BankDetailAPIView.as_view(), name="bank-detail"),
]
