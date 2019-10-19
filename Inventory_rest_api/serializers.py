from rest_framework import serializers
from .models import ProductModel,ProductImageModel,StockModel,CustomerModel,SellModel,BuyModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = (
            'product_id',
            'product_name',
            'product_description',
            'category',
            )

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockModel
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = '__all__'

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellModel
        fields = '__all__'

class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyModel
        fields = '__all__'

