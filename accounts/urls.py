from django.urls import path

from accounts.views import AccountListAPIView, AccountRetrieveUpdateDestroyAPIView, AccountBalanceUpdateAPIView


app_name = "accounts"

urlpatterns = [
    path("", AccountListAPIView.as_view(), name="account-list"),
    path("<int:pk>/", AccountRetrieveUpdateDestroyAPIView.as_view(), name="account-detail"),
    path("<int:pk>/balance/", AccountBalanceUpdateAPIView.as_view(), name="account-balance"),
]
