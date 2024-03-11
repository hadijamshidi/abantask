from django.db import models
from base_models import DateTimeBaseModel
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class StatusChoice(models.TextChoices):
    OPEN = 'OPEN', _('OPEN')
    CLOSED = 'CLOSED', _('CLOSED')


class Buy(DateTimeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symbol = models.CharField(default='', max_length=30, null=True, blank=True)
    status = models.CharField(choices=StatusChoice.choices, default=StatusChoice.OPEN, max_length=20, null=True, blank=True)
    amount = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)

    class Meta:
        ordering = ['-id']