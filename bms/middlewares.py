from constance import config
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from bms.constants import EXEMPT_PATH_PREFIXES


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if config.MAINTENANCE_MODE and not self.is_exempt(request):
            return HttpResponse(
                "The system is currently under maintenance. Please try again later.",
                status=503,
            )

        return self.get_response(request)

    def is_exempt(self, request):
        if request.path.startswith(EXEMPT_PATH_PREFIXES):
            return True

        return self.is_staff(request)

    def is_staff(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return True

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Token "):
            return False

        token_key = auth_header.split("Token ")[1]
        token = Token.objects.filter(key=token_key).select_related("user").first()

        return bool(token and token.user.is_staff)
