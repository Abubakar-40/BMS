from datetime import datetime

from django.db.models import Case, DecimalField, F, Max, Sum, When, Window
from django.utils import timezone

from accounts.models import Transaction


def get_account_summary(account_id, year=None, month=None):
    all_transactions = Transaction.objects.filter(account_id=account_id)
    period_transactions = all_transactions
    prior_transactions = Transaction.objects.none()

    if year:
        period_transactions = period_transactions.filter(created__year=year)
        period_start = timezone.make_aware(datetime(year, month or 1, 1))
        prior_transactions = all_transactions.filter(created__lt=period_start)

    if month:
        period_transactions = period_transactions.filter(created__month=month)

    signed_amount = Case(
        When(type="DEPOSIT", then=F("amount")),
        When(type="WITHDRAWAL", then=-F("amount")),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )

    opening_balance = prior_transactions.aggregate(total=Sum(signed_amount))["total"] or 0

    totals = period_transactions.aggregate(
        total_deposits=Sum(
            Case(
                When(type="DEPOSIT", then=F("amount")),
                default=0,
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        ),
        total_withdrawals=Sum(
            Case(
                When(type="WITHDRAWAL", then=F("amount")),
                default=0,
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        ),
        max_txn_amount=Max("amount"),
    )

    running_totals = period_transactions.annotate(
        running_total=Window(
            expression=Sum(signed_amount),
            order_by=[F("created").asc(), F("id").asc()],
        ),
    ).values_list("running_total", flat=True)

    running_balances = [opening_balance + running_total for running_total in running_totals]
    min_running_balance = min(running_balances) if running_balances else opening_balance

    return {
        "opening_balance": opening_balance,
        "total_deposits": totals["total_deposits"] or 0,
        "total_withdrawals": totals["total_withdrawals"] or 0,
        "max_txn_amount": totals["max_txn_amount"] or 0,
        "min_running_balance": min_running_balance,
    }
