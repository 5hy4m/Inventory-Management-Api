from .views import *
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns 
router = routers.DefaultRouter()
router.register('Product',ProductApiView,basename='Product')
router.register('ProductImage',ProductImageViewset)
router.register('Stock',StockViewset)
router.register('Customer',CustomerViewset)
router.register('Sell',SaleViewset)
router.register('Buy',PurchaseViewset)

urlpatterns = [
    path('Product/',ProductApiView.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls

# urlpatterns = [
#     path('Product/',ProductApiView.as_view()),
#     path('ProductImage',ProductImageViewset.as_view()),
#     path('Stock',StockViewset.as_view()),
#     path('Customer',CustomerViewset.as_view()),
#     path('Sell',SaleViewset.as_view()),
#     path('Buy',PurchaseViewset.as_view()),
# ]
# print(urlpatterns)