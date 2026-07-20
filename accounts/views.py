from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import Account
from users.decorators import api_login_required


@method_decorator(api_login_required, name="dispatch")
class AccountListView(View):
    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user).select_related("branch__bank")
        data = list(accounts.values("branch__bank__name", "account_number", "balance"))

        return JsonResponse(data, safe=False)
