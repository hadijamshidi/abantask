import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aban.settings')
django.setup()
from django.contrib.auth.models import User
from exchange.models import Wallet
from exchange.enums import Quote
from decimal import Decimal

def create_fake_users():
    usernames = ['user1', 'user2']
    password = 'aA@123456'
    for username in usernames:
        user, _ = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()
        user_wallet, _ = Wallet.objects.get_or_create(user=user, asset=Quote.USD)
        user_wallet.balance += Decimal('100.0')
        user_wallet.save()

        
if __name__ == '__main__':
    create_fake_users()
