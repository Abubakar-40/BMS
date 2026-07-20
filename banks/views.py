from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from banks.models import Bank
from users.decorators import api_login_required


@method_decorator(api_login_required, name="dispatch")
class BankListView(View):
    def get(self, request, *args, **kwargs):
        banks = Bank.objects.annotate(branch_count=Count("branches"))
        data = list(banks.values("name", "is_islamic", "branch_count"))

        return JsonResponse(data, safe=False)
