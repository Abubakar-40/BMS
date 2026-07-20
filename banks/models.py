from django.db import models

from bms.models import BaseModel


class Bank(BaseModel):
    name = models.CharField(max_length=255)
    swift_code = models.CharField(max_length=55, unique=True)
    is_islamic = models.BooleanField(default=False)
    established_date = models.DateField()

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
        db_table = "banks"

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)

    bank = models.ForeignKey("banks.Bank", on_delete=models.CASCADE, related_name="branches")

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        db_table = "branches"

    def __str__(self):
        branch_label = f"{self.name} ({self.bank.name})"

        return branch_label
