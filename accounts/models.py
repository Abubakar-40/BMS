from django.db import models

from accounts.choices import AccountType


class Account(models.Model):
    account_number = models.CharField(max_length=31, unique=True)
    account_type = models.CharField(max_length=31, choices=AccountType.choices)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="accounts")
    branch = models.ForeignKey("banks.Branch", on_delete=models.CASCADE, related_name="accounts")

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = "accounts"

    def __str__(self):
        return self.account_number
