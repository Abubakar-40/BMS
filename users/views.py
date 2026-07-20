from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"detail": "Invalid credentials"}, status=401)
        login(request, user)

        return JsonResponse({"detail": "Login successful", "username": user.username})


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)

        return JsonResponse({"detail": "Logout successful"})
