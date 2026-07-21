from django.contrib import admin

from accounts.models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "user", "branch", "account_type", "balance", "is_active")
    list_filter = ("account_type", "is_active", "branch__bank")
    search_fields = ("account_number", "user__username", "user__email")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "type", "amount", "created")
    list_filter = ("type", "created")
    search_fields = ("account__account_number",)
