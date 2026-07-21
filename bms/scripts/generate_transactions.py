import random
from datetime import date, timedelta

from accounts.choices import AccountType, TransactionType
from accounts.models import Account, Transaction
from banks.models import Bank, Branch
from users.models import User


deleted_banks = Bank.objects.all().delete()
deleted_users = User.objects.filter(is_superuser=False).delete()

bank_names = ("Meezan Bank", "HBL", "UBL", "Bank Alfalah")

banks = []
for index, name in enumerate(bank_names):
    bank = Bank.objects.create(
        name=name,
        swift_code=f"SWIFT{index:04d}",
        is_islamic=index % 2 == 0,
        established_date=date(2000 + index, 1, 1),
    )
    banks.append(bank)

branches = []
for bank in banks:
    branch = Branch.objects.create(
        bank=bank,
        name=f"{bank.name} Main Branch",
        branch_code=f"{bank.swift_code}-001",
        address="Sample Address",
    )
    branches.append(branch)

users = []
for index in range(1, 11):
    user = User.objects.create_user(
        username=f"user{index}",
        password="Password123!",
        first_name=f"First{index}",
        last_name=f"Last{index}",
    )
    users.append(user)

start_date = date(2024, 1, 1)
end_date = date(2025, 12, 31)
date_range_days = (end_date - start_date).days

accounts = []
for user in users:
    bank_indexes = random.sample(range(len(banks)), 2)
    for bank_index in bank_indexes:
        branch = branches[bank_index]
        account = Account.objects.create(
            user=user,
            branch=branch,
            account_number=f"ACC-{user.id:03d}-{bank_index}",
            account_type=random.choice(AccountType.values),
            balance=random.randint(1000, 50000),
        )
        accounts.append(account)

transactions = []
for account in accounts:
    transaction_count = random.randint(30, 50)
    for _ in range(transaction_count):
        random_days = random.randint(0, date_range_days)
        transaction_date = start_date + timedelta(days=random_days)
        transaction = Transaction(
            account=account,
            date=transaction_date,
            amount=random.randint(100, 20000),
            type=random.choice(TransactionType.values),
        )
        transactions.append(transaction)

created_transactions = Transaction.objects.bulk_create(transactions)

print("banks created:", Bank.objects.count())
print("branches created:", Branch.objects.count())
print("users created:", User.objects.filter(is_superuser=False).count())
print("accounts created:", Account.objects.count())
print("transactions created:", Transaction.objects.count())
