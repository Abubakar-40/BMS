from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source="branch.bank.name", read_only=True)

    class Meta:
        model = Account
        fields = ("id", "account_number", "account_type", "balance", "is_active", "bank_name")
