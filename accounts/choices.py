from django.db import models


class AccountType(models.TextChoices):
    SAVINGS = "SAVINGS", "Savings"
    CURRENT = "CURRENT", "Current"
