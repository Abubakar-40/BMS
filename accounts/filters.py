import django_filters

from accounts.models import Account


class AccountFilter(django_filters.FilterSet):
    bank = django_filters.NumberFilter(field_name="branch__bank")
    is_islamic = django_filters.BooleanFilter(field_name="branch__bank__is_islamic")

    class Meta:
        model = Account
        fields = ("bank", "account_type", "is_islamic")
