from rest_framework.routers import DefaultRouter
from .apis import BuyViewSet, WalletViewSet


router = DefaultRouter()
router.register('buy', BuyViewSet, basename='buy')
router.register('wallet', WalletViewSet, basename='wallet')


urlpatterns = [] 
urlpatterns += router.urls
