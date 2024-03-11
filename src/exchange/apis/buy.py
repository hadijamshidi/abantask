from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions
from ..models import Buy
from ..schemas import BuySerializer



class BuyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
    ):

    serializer_class = BuySerializer
    need_authentication = True
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Buy.objects.filter(user=self.request.user)
