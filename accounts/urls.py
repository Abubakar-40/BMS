from django.urls import path

from accounts.views import AccountListAPIView, AccountListGenericAPIView


app_name = "accounts"

urlpatterns = [
    path("", AccountListAPIView.as_view(), name="account-list"),
    path("generic/", AccountListGenericAPIView.as_view(), name="account-list-generic"),
]
