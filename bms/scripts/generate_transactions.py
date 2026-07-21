import random
from datetime import date, datetime, timedelta

from django.utils import timezone

from accounts.choices import AccountType, TransactionType
from accounts.models import Account, Transaction
from banks.models import Bank, Branch
from users.models import User


def create_banks_and_branches():
    bank_names = ("Meezan Bank", "HBL", "UBL", "Bank Alfalah")
    banks = []
    branches = []
    for index, name in enumerate(bank_names):
        bank = Bank.objects.create(
            name=name,
            swift_code=f"SWIFT{index:04d}",
            is_islamic=index % 2 == 0,
            established_date=date(2000 + index, 1, 1),
        )
        branch = Branch.objects.create(
            bank=bank,
            name=f"{bank.name} Main Branch",
            branch_code=f"{bank.swift_code}-001",
            address="Sample Address",
        )
        banks.append(bank)
        branches.append(branch)

    return banks, branches


def create_users():
    users = []
    for index in range(1, 11):
        user = User.objects.create_user(
            username=f"user{index}",
            password="Password123!",
            first_name=f"First{index}",
            last_name=f"Last{index}",
        )
        users.append(user)

    return users


def create_accounts(users, branches):
    accounts = []
    for user in users:
        bank_indexes = random.sample(range(len(branches)), 2)
        for bank_index in bank_indexes:
            account = Account.objects.create(
                user=user,
                branch=branches[bank_index],
                account_number=f"ACC-{user.id:03d}-{bank_index}",
                account_type=random.choice(AccountType.values),
                balance=random.randint(1000, 50000),
            )
            accounts.append(account)

    return accounts


def create_transactions(accounts):
    start_date = date(2024, 1, 1)
    date_range_days = (date(2025, 12, 31) - start_date).days
    transactions = []
    for account in accounts:
        transaction_count = random.randint(30, 50)
        for _ in range(transaction_count):
            transaction_date = start_date + timedelta(days=random.randint(0, date_range_days))
            transaction_created = timezone.make_aware(datetime.combine(transaction_date, datetime.min.time()))
            transaction = Transaction(
                account=account,
                created=transaction_created,
                amount=random.randint(100, 20000),
                type=random.choice(TransactionType.values),
            )
            transactions.append(transaction)

    return Transaction.objects.bulk_create(transactions)


deleted_banks = Bank.objects.all().delete()
deleted_users = User.objects.filter(is_superuser=False).delete()

banks, branches = create_banks_and_branches()
users = create_users()
accounts = create_accounts(users, branches)
created_transactions = create_transactions(accounts)

print("banks created:", Bank.objects.count())
print("branches created:", Branch.objects.count())
print("users created:", User.objects.filter(is_superuser=False).count())
print("accounts created:", Account.objects.count())
print("transactions created:", Transaction.objects.count())
