from decimal import Decimal
from django.db import transaction as tr
from rest_framework.serializers import ModelSerializer, ValidationError
from ..logics import get_price
from ..models import Buy, Wallet
from ..enums import Quote
from ..tasks import settelment


class BuySerializer(ModelSerializer):
    class Meta:
        model = Buy
        exclude = ['user']
        extra_kwargs = {
            'amount': {'required': True, 'min_value': Decimal('0.0')},
            'symbol': {'required': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate_symbol(self, symbol):
        if not symbol == symbol.upper():
            raise ValidationError("must be upper case") 
        return symbol

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get('request').user
        amount = attrs['amount']
        symbol = attrs['symbol']
        price = get_price(symbol=symbol)
        self.required_balance = price * amount
        usd_wallet = Wallet.objects.filter(user=user, asset=Quote.USD, balance__gte=self.required_balance).first()
        if not usd_wallet:
            raise ValidationError('insufficient account balance')
        _, _ = Wallet.objects.get_or_create(user=user, asset=symbol)
        return attrs
    
    @tr.atomic()    
    def create(self, validated_data):
        amount = validated_data['amount']
        symbol = validated_data['symbol']
        price = get_price(symbol=symbol)
        required_balance = price * amount
        user = self.context.get('request').user
        user_wallets = Wallet.objects.filter(user=user).select_for_update()
        usd_wallet = user_wallets.filter(asset=Quote.USD).first()
        usd_wallet.balance -= required_balance
        usd_wallet.save()
        buy = Buy.objects.create(user=user, **validated_data) 
        symbol_wallet = user_wallets.filter(asset=symbol).first()
        symbol_wallet.balance += amount
        symbol_wallet.save()
        tr.on_commit(lambda: settelment.delay(
                symbol=symbol
        ))
        return buy
