from .views import *
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns 
router = routers.DefaultRouter()
router.register('organization',OrganizationViewset)
router.register('customer',CustomerViewset,basename='customer')
router.register('vendor',VendorViewset,basename='vendor')
router.register('product',ProductViewset,basename='Product')
router.register('productgroup',ProductGroupViewset,basename='Productgroup')
router.register('productImage',ProductImageViewset)
router.register('stock',StockViewset)
router.register('saleorderproducts',SalesProductsViewset,basename = 'salesorderproducts')
router.register('salesorder',SalesOrderViewset)
router.register('purchaseproducts',PurchaseProductsViewset)
router.register('purchaseorder',PurchaseOrderViewset)
router.register('activity',ActivityViewset)
router.register('invoice',InvoiceViewset)
router.register('invoiceproducts',InvoiceProductsViewset)
router.register('bill',BillViewset)
router.register('billproducts',BillProductsViewset)

urlpatterns = [
    
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
