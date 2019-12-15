from .models import *
from .serializers import *
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# Create your views here.
class ProductApiView(APIView):

    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request, format=None):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None,pk = None):
        print("Requested DATA",request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer

class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer

class StockViewset(viewsets.ModelViewSet):
    queryset = StockModel.objects.all()
    serializer_class = StockSerializer

class CustomerViewset(viewsets.ModelViewSet):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer

    def list(self,request):
        serializer =  self.get_serializer(self.queryset,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        print("GOT REQUEST :",request)
        serializer = self.get_serializer(data = request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaleViewset(viewsets.ModelViewSet):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer

class PurchaseViewset(viewsets.ModelViewSet):
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseSerializer