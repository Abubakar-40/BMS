from django.urls import path

from accounts.views import AccountListAPIView, AccountListGenericView


app_name = "accounts"

urlpatterns = [
    path("", AccountListAPIView.as_view(), name="account-list"),
    path("generic/", AccountListGenericView.as_view(), name="account-list-generic"),
]
