from django.urls import path

from accounts.views import (
    AccountListAPIView,
    AccountRetrieveUpdateDestroyAPIView,
    AccountBalanceUpdateAPIView,
    AccountSummaryAPIView,
)


app_name = "accounts"

urlpatterns = [
    path("", AccountListAPIView.as_view(), name="account-list"),
    path("<int:pk>/", AccountRetrieveUpdateDestroyAPIView.as_view(), name="account-retrieve-update-destroy"),
    path("<int:pk>/balance/", AccountBalanceUpdateAPIView.as_view(), name="account-balance-update"),
    path("<int:pk>/summary/", AccountSummaryAPIView.as_view(), name="account-summary"),
]
