from django.db import models

from accounts.choices import AccountType
from bms.models import BaseModel


class Account(BaseModel):
    account_number = models.CharField(max_length=55, unique=True)
    account_type = models.CharField(max_length=55, choices=AccountType.choices, default=AccountType.SAVINGS)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="accounts")
    branch = models.ForeignKey("banks.Branch", on_delete=models.CASCADE, related_name="accounts")

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        db_table = "accounts"

    @property
    def bank_name(self):
        return self.branch.bank.name

    def __str__(self):
        return self.account_number
