from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = '__all__'

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddressModel
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroupModel
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockModel
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = '__all__'

class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddressModel
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleModel
        fields = '__all__'

class SaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderModel
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseModel
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    # products = InvoiceProductsSerializer(many=True)
    class Meta:
        model = InvoiceModel
        fields = '__all__'
        # fields = [
        #     'invoice_no',
        #     'customer_id',
        #     'invoice_date',
        #     'due_date',
        #     'customer_notes',
        #     'terms_and_conditions',
        # ]

class InvoiceProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProductsModel
        fields = ['invoice_no','product_id']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityModel
        fields = '__all__'
