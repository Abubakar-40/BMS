from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "user", "branch", "account_type", "balance", "is_active")
    list_filter = ("account_type", "is_active", "branch__bank")
    search_fields = ("account_number", "user__username", "user__email")
