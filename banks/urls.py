from django.urls import path

from banks.views import BankListAPIView, BankListGenericView


app_name = "banks"

urlpatterns = [
    path("", BankListAPIView.as_view(), name="bank-list"),
    path("generic/", BankListGenericView.as_view(), name="bank-list-generic"),
]
