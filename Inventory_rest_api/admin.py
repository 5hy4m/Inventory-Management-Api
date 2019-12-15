from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ProductModel)
admin.site.register(ProductImageModel)
admin.site.register(StockModel)
admin.site.register(CustomerModel)
admin.site.register(SaleModel)
admin.site.register(PurchaseModel)
admin.site.register(ProductGroupModel)
admin.site.register(CustomerAddressModel)
admin.site.register(VendorModel)
admin.site.register(VendorAddressModel)
admin.site.unregister(SaleModel)
admin.site.register(SaleModel)
admin.site.register(SalesOrderModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(InvoiceModel)
admin.site.register(ActivitiesModel)
