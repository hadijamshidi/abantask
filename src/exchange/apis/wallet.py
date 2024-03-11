from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions
from ..models import Wallet
from ..schemas import WalletSerializer



class WalletViewSet(ReadOnlyModelViewSet):

    serializer_class = WalletSerializer
    need_authentication = True
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
