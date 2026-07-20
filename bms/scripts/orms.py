from django.db.models import Count

from accounts.models import Account
from banks.models import Bank


print("All banks")
print(list(Bank.objects.all()))

print("Islamic banks")
print(list(Bank.objects.filter(is_islamic=True)))

print("Get bank by swift code")
print(Bank.objects.get(swift_code="MEZNPKKA"))

print("Bank values name and is_islamic")
print(list(Bank.objects.values("name", "is_islamic")))

print("Accounts with select_related")
accounts = Account.objects.select_related("user", "branch__bank").all()
for account in accounts:
    print(account.account_number, account.user.username, account.branch.bank.name)

print("Banks annotated with account count")
banks_with_count = Bank.objects.annotate(account_count=Count("branches__accounts"))
for bank in banks_with_count:
    print(bank.name, bank.account_count)

print("Islamic banks with active accounts")
print(list(Bank.objects.filter(is_islamic=True, branches__accounts__is_active=True).distinct()))
