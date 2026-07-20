from django.contrib import admin

from banks.models import Bank, Branch


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "swift_code", "is_islamic", "established_date")
    list_filter = ("is_islamic",)
    search_fields = ("name", "swift_code")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "branch_code", "bank", "address")
    list_filter = ("bank",)
    search_fields = ("name", "branch_code", "bank__name")
