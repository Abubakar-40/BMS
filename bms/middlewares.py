from constance import config
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.authtoken.models import Token


class MaintenanceModeMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if not config.MAINTENANCE_MODE or request.path.startswith(("/admin/", "/api/auth/login/")):
            return self.get_response(request)

        token_key = request.headers.get("Authorization", "").replace("Token ", "")
        if request.user.is_staff or Token.objects.filter(key=token_key, user__is_staff=True).exists():
            return self.get_response(request)

        return HttpResponse(
            "The system is currently under maintenance. Please try again later.",
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
