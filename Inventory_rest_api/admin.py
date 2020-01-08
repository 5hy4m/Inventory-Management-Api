from django.contrib import admin
from .models import *
# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'commited', 'quantity','location')

# To Show PRimary key
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('product_id',) 

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('ids','activity_name','Date','Time')

admin.site.register(OrganizationModel)
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
admin.site.register(InvoiceProductsModel)
admin.site.register(ActivityModel,ActivityAdmin)
admin.site.register(StockModel, StockAdmin)
admin.site.register(AddressModel)
