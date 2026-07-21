from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.filters import AccountFilter
from accounts.models import Account
from accounts.permissions import IsStaffForRetrieveDelete
from accounts.serializers import AccountSerializer, AccountBalanceSerializer


class AccountListAPIView(ListCreateAPIView):
    serializer_class = AccountSerializer
    filterset_class = AccountFilter
    search_fields = ("user__first_name", "user__last_name", "user__username")
    ordering_fields = ("balance", "created", "user__username")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).select_related("branch__bank")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsStaffForRetrieveDelete)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all().select_related("branch__bank")

        return Account.objects.filter(user=self.request.user).select_related("branch__bank")


class AccountBalanceAPIView(UpdateAPIView):
    serializer_class = AccountBalanceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()

        return Account.objects.filter(user=self.request.user)
