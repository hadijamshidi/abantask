from aban.celery import app
from .logics import exchange_settelment



@app.task
def settelment(symbol):
    exchange_settelment(symbol=symbol)
    return symbol
