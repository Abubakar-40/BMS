from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.filters import AccountFilter
from accounts.models import Account
from accounts.permissions import IsStaffForRetrieveDelete
from accounts.reports import get_account_summary
from accounts.serializers import AccountSerializer, AccountBalanceSerializer, AccountSummarySerializer


class AccountListAPIView(ListCreateAPIView):
    serializer_class = AccountSerializer
    filterset_class = AccountFilter
    search_fields = ("user__first_name", "user__last_name", "user__username")
    ordering_fields = ("balance", "created", "user__username")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).select_related("branch__bank")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsStaffForRetrieveDelete)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all().select_related("branch__bank")

        return Account.objects.filter(user=self.request.user).select_related("branch__bank")


class AccountBalanceUpdateAPIView(UpdateAPIView):
    serializer_class = AccountBalanceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()

        return Account.objects.filter(user=self.request.user)


class AccountSummaryAPIView(APIView):
    def get(self, request, account_id, *args, **kwargs):
        year = request.query_params.get("year")
        month = request.query_params.get("month")

        if month and not year:
            return Response(
                {"detail": "month filter requires year to also be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        account = get_object_or_404(Account.objects.filter(user=request.user), id=account_id)
        summary = get_account_summary(
            account.id,
            year=int(year) if year else None,
            month=int(month) if month else None,
        )
        serializer = AccountSummarySerializer(summary)

        return Response(serializer.data, status=status.HTTP_200_OK)
