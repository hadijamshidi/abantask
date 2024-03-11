from django.conf import settings
from django.db import transaction as tr
from django.db.models import Sum
from ..models import Buy, StatusChoice
from .market import get_price


def buy_from_exchange(symbol, amount):
    return True


@tr.atomic()
def exchange_settelment(symbol):
    price = get_price(symbol=symbol)
    min_required_notional_value = settings.EXCHANGE_MIN_NOTIONAL_VALUE
    open_orders = Buy.objects.filter(symbol=symbol, status=StatusChoice.OPEN).select_for_update()
    open_orders_total_amount = open_orders.aggregate(total_amount=Sum('amount'))['total_amount']
    if open_orders_total_amount * price > min_required_notional_value:
        result = buy_from_exchange(symbol=symbol, amount=float(open_orders_total_amount))
        if result:
            open_orders.update(status=StatusChoice.CLOSED)
