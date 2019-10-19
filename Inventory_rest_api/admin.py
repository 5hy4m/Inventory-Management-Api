from django.contrib import admin
from .models import ProductModel,ProductImageModel,StockModel,CustomerModel,SellModel,BuyModel
# Register your models here.
admin.site.register(ProductModel)
admin.site.register(ProductImageModel)
admin.site.register(StockModel)
admin.site.register(CustomerModel)
admin.site.register(SellModel)
admin.site.register(BuyModel)
