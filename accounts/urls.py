from django.urls import path

from accounts.views import AccountListAPIView, AccountDetailAPIView, AccountBalanceAPIView


app_name = "accounts"

urlpatterns = [
    path("", AccountListAPIView.as_view(), name="account-list"),
    path("<int:pk>/", AccountDetailAPIView.as_view(), name="account-detail"),
    path("<int:pk>/balance/", AccountBalanceAPIView.as_view(), name="account-balance"),
]
