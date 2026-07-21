from django.urls import path

from banks.views import BankListAPIView, BankRetrieveUpdateDestroyAPIView


app_name = "banks"

urlpatterns = [
    path("", BankListAPIView.as_view(), name="bank-list"),
    path("<int:pk>/", BankRetrieveUpdateDestroyAPIView.as_view(), name="bank-retrieve-update-destroy"),
]
