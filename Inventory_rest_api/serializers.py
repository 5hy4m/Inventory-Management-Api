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

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockModel
        fields = ['quantity','product_id','location','commited']
        read_only_fields = ('product_id',)

class ProductSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=False)   
    class Meta:
        model = ProductModel
        fields = ['group_id','product_id','product_name','product_description','stocks']
        read_only_fields = ('product_id',)

    def create(self, validated_data):
        stock_data = validated_data.pop('stocks')
        product = ProductModel.objects.create(**validated_data)#To get pk of the instance
        StockModel.objects.create(product_id = product,**stock_data)
        return product

    def update(self,instance,validated_data):
        print("inside update metod of serializer")
        print('INSTANCE : ',instance)
        nested_data = validated_data.pop('stocks')
        product = ProductModel.objects.create(**validated_data)
        ###updating parent 
        instance.group_id = validated_data['group_id']
        instance.product_id = validated_data['product_id']
        instance.product_name = validated_data['product_name']
        instance.product_description = validated_data['product_description']
        ### updating nested value ###
        
        product.stocks.add(nested_data)
        print("Stocks data : ",validated_data)

        return instance

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroupModel
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
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

class InvoiceProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProductsModel
        fields = ['invoice_no','product_id']

class InvoiceSerializer(serializers.ModelSerializer):
    products = InvoiceProductsSerializer(many=True)
    class Meta:
        model = InvoiceModel
        fields = '__all__'
        read_only_fields = ('invoice_no',)

    def create(self, validated_data):
        products_data = validated_data.pop('stocks')
        invoice = InvoiceModel.objects.create(**validated_data)#To get pk of the instance
        InvoiceProductsModel.objects.create(invoice_no = invoice,**products_data)
        return invoice

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityModel
        fields = '__all__'
