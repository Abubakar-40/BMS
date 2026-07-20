from django.urls import path

from banks.views import BankListAPIView, BankListGenericAPIView


app_name = "banks"

urlpatterns = [
    path("", BankListAPIView.as_view(), name="bank-list"),
    path("generic/", BankListGenericAPIView.as_view(), name="bank-list-generic"),
]
