from rest_framework import serializers
from .models import *
import datetime as dt
import calendar

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
        print('INSTANCE : ',instance.product_id)
        # stock = instance.stocks.all()
        ###updating parent 
        instance.group_id = validated_data['group_id']
        instance.product_id = instance.product_id
        instance.product_name = validated_data['product_name']
        instance.product_description = validated_data['product_description']
        instance.save()
        ### updating nested value ###
        StockModel.objects.filter(product_id =instance.product_id ).update(**nested_data)
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
        fields = ['product_id','invoice_id']
        read_only_fields = ('invoice_id',)

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_products = InvoiceProductsSerializer(many=True)
    class Meta:
        model = InvoiceModel
        fields = '__all__'
        read_only_fields = ('invoice_no',)
    
    def getNewInvoiceNo(self,restart,previous,code):
        if(restart):
            n = 0
            restart = False
            # print("n value while restart: ",n)
        else:
            n = previous
            n= n + 1
            # print("n value : ",n)  
        return str(str(code)+str(n))

    def fiscal_detail(self,organization,current_date,new):
            if new == True:
                print("GENERATING FISCAL YEAR")
                fiscal_detail = organization.fiscal_detail
                fiscal_detail = fiscal_detail.split("-") #GETTING fiscal detail
                fiscal_start_month = int(fiscal_detail[0])
                fiscal_end_month = int(fiscal_detail[1])
                fiscal_end_year = current_date.year if (fiscal_end_month == 12) else current_date.year+1
                last_day_of_fiscal_endmonth = (calendar.monthrange(fiscal_end_year,fiscal_end_month))[1]
                last_date_of_fiscal_endyear = dt.datetime(fiscal_end_year, fiscal_end_month, last_day_of_fiscal_endmonth)
                OrganizationModel.objects.filter(pk=1).update(fiscal_end = last_date_of_fiscal_endyear)
            else:
                return OrganizationModel.objects.first().fiscal_end
                
    def create(self, validated_data):
        current_date = dt.datetime.now()
        # current_date = dt.datetime(2021,1,1)
        current_date = dt.datetime(current_date.year, current_date.month, current_date.day)#CREATING A DATE OBJECT
        organization = OrganizationModel.objects.first()
        code = organization.invoice_code
        invoices_objects = InvoiceModel.objects.last()


        if not invoices_objects:
            # print("There IS No objects in invoice")
            previous = 1
            restart = True
            last_date_of_fiscal_year = self.fiscal_detail(organization,current_date,new = True)
        elif (current_date <= dt.datetime.strptime(organization.fiscal_end, '%Y-%m-%d %H:%M:%S')):
            # print("DOnt Restart")
            # invoices_objects = InvoiceModel.objects.order_by('-id')[0]
            previous = invoices_objects.invoice_no
            print("Previous invoice number : ",previous.split("-")[1])
            previous = int(previous.split("-")[1])
            restart = False
        else:
            invoice_id_activity = ActivityModel.objects.filter(activity_name__icontains = 'invoice').latest('Date','Time')
            invoice_id_activity = invoice_id_activity.ids.split("-")[0]
            if invoice_id_activity == organization.invoice_code[0:-1]:
                raise serializers.ValidationError('Please Change the Invoice code,Sales code,purchase code')
            restart = True
            previous = 1
            last_date_of_fiscal_year = self.fiscal_detail(organization,current_date,new = True)

            
        ### function CAll
        previous = self.getNewInvoiceNo(restart,previous,code)# THIS IS THE INVOICE NUMBER
        products_data = validated_data.pop('invoice_products')    
        validated_data['invoice_no'] = previous
        # print("validated_data",validated_data,sep = " : ")
        invoice = InvoiceModel.objects.create(**validated_data)#To get pk of the instance
        # print("populated in invoice Model yet to populate in invoiceproducts Model")
        for product in products_data:
            InvoiceProductsModel.objects.create(invoice_id = invoice,**product)
        return invoice

    def update(self,instance,validated_data):
        print("inside update method of serializer")
        # print('INSTANCE : ',validated_data)
        nested_data = validated_data.pop('invoice_products')
        invoice_products = (instance.invoice_products).all()
        invoice_products = list(invoice_products)
        print('INSTANCE : ',nested_data)
        print()
        ###updating parent 
        instance.invoice_no = int(instance.invoice_no)
        instance.customer_id = validated_data['customer_id']
        instance.due_date = validated_data['due_date']
        instance.invoice_status = validated_data['invoice_status']
        instance.customer_notes = validated_data['customer_notes']
        instance.terms_and_conditions = validated_data['terms_and_conditions']
        instance.save()
        ### updating nested value ###
        print("pk value :",int(instance.invoice_no))
        for data in nested_data:
            invoice_product = invoice_products.pop(0)
            invoice_product.product_id = data.get('product_id')
            invoice_product.save()
        return instance
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityModel
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = '__all__'

