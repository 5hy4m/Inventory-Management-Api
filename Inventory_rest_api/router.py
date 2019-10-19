from .views import ProductViewet,ProductImageViewset,StockViewset,CustomerViewset,SellViewset,BuyViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Product',ProductViewet)
router.register('ProductImage',ProductImageViewset)
router.register('Stock',StockViewset)
router.register('Customer',CustomerViewset)
router.register('Sell',SellViewset)
router.register('Buy',BuyViewset)

# urlpatterns = router.urls