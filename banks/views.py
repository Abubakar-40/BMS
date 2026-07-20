from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from banks.models import Bank
from banks.serializers import BankSerializer
from users.decorators import api_login_required


@method_decorator(api_login_required, name="dispatch")
class BankListView(View):
    def get(self, request, *args, **kwargs):
        banks = Bank.objects.annotate(branch_count=Count("branches"))
        data = list(banks.values("name", "is_islamic", "branch_count"))

        return JsonResponse(data, safe=False)


class BankListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)

        return Response(serializer.data)


class BankListGenericAPIView(ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
