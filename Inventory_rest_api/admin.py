from django.contrib import admin
from .models import *
# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'commited', 'quantity','location')

# To Show PRimary key
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('product_id',) 

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('ids','activity_name','date','time')

admin.site.register(OrganizationModel)
admin.site.register(ProductModel,ProductAdmin)
admin.site.register(ProductImageModel)
admin.site.register(CustomerModel)
admin.site.register(ProductGroupModel)
admin.site.register(VendorModel)
admin.site.register(SalesProductsModel)
admin.site.register(SalesOrderModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(PurchaseProductsModel)
admin.site.register(InvoiceModel)
admin.site.register(InvoiceProductsModel)
admin.site.register(ActivityModel,ActivityAdmin)
admin.site.register(StockModel, StockAdmin)
admin.site.register(AddressModel)
admin.site.register(BillModel)
admin.site.register(BillProductsModel)
