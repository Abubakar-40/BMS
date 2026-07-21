from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "account_number", "account_type", "balance", "is_active", "bank_name", "branch")


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "balance")


class AccountSummarySerializer(serializers.Serializer):
    opening_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_deposits = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_withdrawals = serializers.DecimalField(max_digits=12, decimal_places=2)

    max_txn_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    min_running_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
