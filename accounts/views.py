from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from users.decorators import api_login_required


@method_decorator(api_login_required, name="dispatch")
class AccountListView(View):
    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user).select_related("branch__bank")
        data = list(accounts.values("branch__bank__name", "account_number", "balance"))

        return JsonResponse(data, safe=False)


class AccountListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user).select_related("branch__bank")
        serializer = AccountSerializer(accounts, many=True)

        return Response(serializer.data)


class AccountListGenericView(ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).select_related("branch__bank")
