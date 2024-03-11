from django.db import models
from base_models import DateTimeBaseModel
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Wallet(DateTimeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    asset = models.CharField(default='', max_length=30, null=True, blank=True)
    balance = models.DecimalField(default=Decimal('0.0'), decimal_places=5, max_digits=15, null=True, blank=True)

    class Meta:
        ordering = ['-id']