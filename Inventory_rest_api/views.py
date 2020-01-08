from .models import *
from .serializers import *
from django.http import Http404
import json
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import serializers
from django.core import serializers as serial

# Create your views here.

# To Convert QuesryDict to json
#    request_as_json = json.loads(json.dumps(request.data))

# To Convert QuerySet To JSON
    # invoice_json = json.loads(serial.serialize('json',InvoiceModel.objects.filter(customer_id = pk)))

def storeActivity( id, event,description = ""):
        activityobj = ActivityModel.objects.get_or_create(
            ids=id, activity_name=event,description = description)
        print('ACTIVITY Created')
        return

class CustomerViewset(viewsets.ModelViewSet):
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer

    @action(methods=['get'], detail=True,)
    def invoices(self,request,pk=None):
        invoice_json = json.loads(serial.serialize('json',InvoiceModel.objects.filter(customer_id = pk)))
        print("invoice_json : ",invoice_json)
        return Response(invoice_json,status =200)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
          
            serializer.save()
            storeActivity(serializer.data['customer_id'], 'customer added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        print('Destroy')
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        description = request.data['description']
        self.perform_destroy(instance)
        storeActivity(pk, 'customer deleted',description)

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['customer_id'], 'customer updated')

class CustomerAddressViewset(viewsets.ModelViewSet):
    queryset = CustomerAddressModel.objects.all()
    serializer_class = CustomerAddressSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['customer_address_id'], 'customer address added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'customer address deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['customer_address_id'], 'customer address updated')

class VendorViewset(viewsets.ModelViewSet):
    queryset = VendorModel.objects.all()
    serializer_class = VendorSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['vendor_id'], 'vendor added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'vendor deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['vendor_id'], 'vendor updated')

class VendorAddressViewset(viewsets.ModelViewSet):
    queryset = VendorAddressModel.objects.all()
    serializer_class = VendorAddressSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['vendor_address_id'], 'vendor address added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'vendor address deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['vendor_address_id'], 'customer address updated')

class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request.data) #REQUEST IS A QUERY DICT
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ### Storing Activity
            # serializer.instance.product_id to get instance primary key
            storeActivity(serializer.instance.product_id, 'product added')
            ###
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'product deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['product_id'], 'product updated')

class ProductGroupViewset(viewsets.ModelViewSet):
    queryset = ProductGroupModel.objects.all()
    serializer_class = ProductGroupSerializer

    @action(methods=['get'], detail=True,)
    def products(self,request,pk=None):
        items_json = json.loads(serial.serialize('json',ProductModel.objects.filter(group_id = pk)))
        print("itemsOfGroup ",pk," : ",items_json)
        return Response(items_json,status =200)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['group_id'], 'productgroup added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'productgroup deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['group_id'], 'productgroup updated')

class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImageModel.objects.all()
    serializer_class = ProductImageSerializer

class StockViewset(viewsets.ModelViewSet):
    queryset = StockModel.objects.all()
    serializer_class = StockSerializer

    @action(methods=['get'], detail=False,url_path="totalitems")
    def totalItemsInInventory(self,request): 
        TotalProducts = 0
        lists = StockModel.objects.values_list('quantity')
        for i in lists:
            TotalProducts += i[0]
        print('TotalProducts',TotalProducts)
        return Response(TotalProducts,status =200)


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['product_id'], 'stock added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'stock deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['product_id'], 'stock updated')

class SaleViewset(viewsets.ModelViewSet):
    queryset = SaleModel.objects.all()
    serializer_class = SaleSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['sale_id'], 'sale added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'sale deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['sale_id'], 'sale updated')

class SalesOrderViewset(viewsets.ModelViewSet):
    queryset = SalesOrderModel.objects.all()
    serializer_class = SaleOrderSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['sale_order_no'], 'sales order added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'sales order deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['sale_order_no'], 'sales order updated')

class PurchaseViewset(viewsets.ModelViewSet):
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['purchase_id'], 'purchase added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'purchase deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['purchase_id'], 'purchase updated')

class PurchaseOrderViewset(viewsets.ModelViewSet):
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderSerializer


    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.data['purchase_order_no'], 'purchase order added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        self.perform_destroy(instance)
        storeActivity(pk, 'purchase order deleted')

        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['purchase_order_no'], 'purchase order updated')

class InvoiceViewset(viewsets.ModelViewSet):
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        print("LIST IS CALLED")
        return Response(serializer.data)

    def create(self, request):
        print("Create REQUEST :", request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            storeActivity(
                serializer.instance.invoice_no, 'invoice added')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        print('Destroy')
        instance = self.get_object()
        # obj = CustomerModel.objects.filter(pk=pk)
        # serializer = serial.serialize('json',obj)
        print("request.data : ",request.data)
        self.perform_destroy(instance)
        storeActivity(pk, 'invoice deleted')
        return

    def perform_update(self, serializer):
        print('update')
        serializer.save()
        storeActivity(serializer.data['invoice_no'], 'invoice updated')
   
class InvoiceProductsViewset(viewsets.ModelViewSet):
    queryset = InvoiceProductsModel.objects.all()
    serializer_class = InvoiceProductsSerializer

class ActivityViewset(viewsets.ModelViewSet):
    queryset = ActivityModel.objects.all()
    serializer_class = ActivitySerializer

class OrganizationViewset(viewsets.ModelViewSet):
    queryset = OrganizationModel.objects.all()
    serializer_class = OrganizationSerializer
