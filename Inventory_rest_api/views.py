from .models import ProductModel,ProductImageModel,StockModel,CustomerModel,SellModel,BuyModel
from .serializers import ProductSerializer,ProductImageSerializer,StockSerializer,CustomerSerializer,SellSerializer,BuySerializer
from rest_framework import viewsets

# Create your views here.
class ProductViewet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    
class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer

class StockViewset(viewsets.ModelViewSet):
    queryset = StockModel.objects.all()
    serializer_class = StockSerializer

class CustomerViewset(viewsets.ModelViewSet):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer

class SellViewset(viewsets.ModelViewSet):
    queryset = SellModel.objects.all()
    serializer_class = SellSerializer

class BuyViewset(viewsets.ModelViewSet):
    queryset = BuyModel.objects.all()
    serializer_class = BuySerializer