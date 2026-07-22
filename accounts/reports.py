from datetime import datetime, timezone

from django.db.models import Case, DecimalField, F, Max, Sum, Value, When, Window
from django.db.models.functions import Coalesce

from accounts.models import Transaction


DECIMAL_FIELD = DecimalField(max_digits=12, decimal_places=2)


def get_signed_amount():
    return Case(
        When(type="DEPOSIT", then=F("amount")),
        When(type="WITHDRAWAL", then=-F("amount")),
        output_field=DECIMAL_FIELD,
    )


def calculate_opening_balance(account_id, year, month):
    if not year:
        return 0
    period_start = datetime(year, month or 1, 1, tzinfo=timezone.utc)
    prior_transactions = Transaction.objects.filter(account_id=account_id, created__lt=period_start)

    return prior_transactions.aggregate(
        balance=Coalesce(Sum(get_signed_amount()), Value(0), output_field=DECIMAL_FIELD)
    )["balance"]


def calculate_totals(period_transactions):
    return period_transactions.aggregate(
        total_deposits=Coalesce(
            Sum(Case(When(type="DEPOSIT", then=F("amount")), default=0, output_field=DECIMAL_FIELD)),
            Value(0),
            output_field=DECIMAL_FIELD,
        ),
        total_withdrawals=Coalesce(
            Sum(Case(When(type="WITHDRAWAL", then=F("amount")), default=0, output_field=DECIMAL_FIELD)),
            Value(0),
            output_field=DECIMAL_FIELD,
        ),
        max_txn_amount=Coalesce(Max("amount"), Value(0), output_field=DECIMAL_FIELD),
    )


def calculate_min_running_balance(period_transactions, opening_balance):
    running_totals = period_transactions.annotate(
        running_total=Window(expression=Sum(get_signed_amount()), order_by=[F("created").asc(), F("id").asc()]),
    ).values_list("running_total", flat=True)
    running_balances = [opening_balance + running_total for running_total in running_totals]

    return min(running_balances) if running_balances else opening_balance


def get_account_summary(account_id, year=None, month=None):
    period_transactions = Transaction.objects.filter(account_id=account_id)
    if year:
        period_transactions = period_transactions.filter(created__year=year)
    if month:
        period_transactions = period_transactions.filter(created__month=month)

    opening_balance = calculate_opening_balance(account_id, year, month)
    totals = calculate_totals(period_transactions)
    min_running_balance = calculate_min_running_balance(period_transactions, opening_balance)

    return {
        "opening_balance": opening_balance,
        "total_deposits": totals["total_deposits"],
        "total_withdrawals": totals["total_withdrawals"],
        "max_txn_amount": totals["max_txn_amount"],
        "min_running_balance": min_running_balance,
    }
