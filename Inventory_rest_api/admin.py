from django.contrib import admin
from .models import *
# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'commited', 'quantity')

# To Show PRimary key
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('product_id',) 

admin.site.register(ProductModel,ProductAdmin)
admin.site.register(ProductImageModel)
admin.site.register(CustomerModel)
admin.site.register(PurchaseModel)
admin.site.register(ProductGroupModel)
admin.site.register(CustomerAddressModel)
admin.site.register(VendorModel)
admin.site.register(VendorAddressModel)
admin.site.register(SaleModel)
admin.site.register(SalesOrderModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(InvoiceModel)
admin.site.register(ActivityModel)
admin.site.register(StockModel, StockAdmin)

