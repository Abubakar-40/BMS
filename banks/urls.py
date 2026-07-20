from django.urls import path

from banks.views import BankListView


app_name = "banks"

urlpatterns = [
    path("", BankListView.as_view(), name="banks"),
]
