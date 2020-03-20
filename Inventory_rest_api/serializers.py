from rest_framework import serializers
from .models import *
import datetime as dt
import calendar

def getNewNumber(restart,previous,code):
        if(restart):
            n = 1
            restart = False
            # print("n value while restart: ",n)
        else:
            n = previous
            n= n + 1
            # print("n value : ",n)  
        return str(str(code)+str(n))

def fiscalDetail(organization,current_date,new,instance):
        print("GENERATING FISCAL YEAR")
        if instance == None:
            fiscal_detail = organization.fiscal_detail
            fiscal_detail = fiscal_detail.split("-") #GETTING fiscal detail
            fiscal_start_month = int(fiscal_detail[0])
            fiscal_end_month = int(fiscal_detail[1])
        else:
            fiscal_detail = instance
            fiscal_detail = fiscal_detail.split("-") #GETTING fiscal detail
            fiscal_start_month = int(fiscal_detail[0])
            fiscal_end_month = int(fiscal_detail[1])
        if new == True:
            print("Comes under True")
            fiscal_end_year = current_date.year if (fiscal_end_month == 12) else current_date.year+1
            last_day_of_fiscal_endmonth = (calendar.monthrange(fiscal_end_year,fiscal_end_month))[1]
            last_date_of_fiscal_endyear = dt.datetime(fiscal_end_year, fiscal_end_month, last_day_of_fiscal_endmonth)
            OrganizationModel.objects.filter(pk=1).update(fiscal_end = last_date_of_fiscal_endyear)
            return last_date_of_fiscal_endyear
        else:
            print("Comes under False")
            fiscal_end_year = current_date.year
            last_day_of_fiscal_endmonth = (calendar.monthrange(fiscal_end_year,fiscal_end_month))[1]
            last_date_of_fiscal_endyear = dt.datetime(fiscal_end_year, fiscal_end_month, last_day_of_fiscal_endmonth)
            OrganizationModel.objects.filter(pk=1).update(fiscal_end = last_date_of_fiscal_endyear)
            # return OrganizationModel.objects.first().fiscal_end
            return last_date_of_fiscal_endyear

def prefixCodeChecker(organization):
    invoice_prefixcode_from_activity = ActivityModel.objects.filter(activity_name__icontains = 'invoice').latest('date','time')
    invoice_prefixcode_from_activity = None if not invoice_prefixcode_from_activity else invoice_prefixcode_from_activity.ids.split("-")[0] 
    salesorder_prefixcode_from_activity = ActivityModel.objects.filter(activity_name__icontains = 'sales order added').latest('date','time')
    salesorder_prefixcode_from_activity = None if not salesorder_prefixcode_from_activity else salesorder_prefixcode_from_activity.ids.split("-")[0] 
    purchaseorder_prefixcode_from_activity = ActivityModel.objects.filter(activity_name__icontains = 'purchase order added').latest('date','time')
    purchaseorder_prefixcode_from_activity = None if not purchaseorder_prefixcode_from_activity else purchaseorder_prefixcode_from_activity.ids.split("-")[0] 
    bill_prefixcode_from_activity = ActivityModel.objects.filter(activity_name__icontains = 'bill added').latest('date','time')
    bill_prefixcode_from_activity = None if not bill_prefixcode_from_activity else bill_prefixcode_from_activity.ids.split("-")[0]

    if(invoice_prefixcode_from_activity == organization.invoice_code[0:-1]):
        raise serializers.ValidationError('Please Change the Invoice code')
    elif invoice_prefixcode_from_activity == None:
        raise serializers.ValidationError(' there is no invoice avaliable')

    if(salesorder_prefixcode_from_activity == organization.salesorder_code[0:-1]):
        raise serializers.ValidationError('Please Change the Sales code')
    elif salesorder_prefixcode_from_activity == None:
        raise serializers.ValidationError(' there is no salesorder avaliable')

    if(purchaseorder_prefixcode_from_activity == organization.purchaseorder_code[0:-1]):
        raise serializers.ValidationError('Please Change the purchase code')
    elif purchaseorder_prefixcode_from_activity == None:
        raise serializers.ValidationError(' there is no Purchaseorder avaliable')

    if(bill_prefixcode_from_activity == organization.bill_code[0:-1]):
        raise serializers.ValidationError('Please Change the Bill code')
    elif bill_prefixcode_from_activity == None:
        raise serializers.ValidationError(' there is no bill avaliable')
    
    # activity_id = ActivityModel.objects.filter(activity_name__icontains = 'sale_id').latest('Date','Time')
    # sales order added

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
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
        fields = '__all__'
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
        StockModel.objects.filter(product_id =instance.product_id).update(**nested_data)
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

class SaleProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesProductsModel
        fields = '__all__'

class SaleOrderSerializer(serializers.ModelSerializer):
    sales_products = SaleProductsSerializer(many=True)
    class Meta:
        model = SalesOrderModel
        fields = '__all__'
        read_only_fields = ('sales_order_no',)


    def create(self, validated_data):
        current_date = dt.datetime.now()
        # current_date = dt.datetime(2021,1,1)
        current_date = dt.datetime(current_date.year, current_date.month, current_date.day)#CREATING A DATE OBJECT
        organization = OrganizationModel.objects.first()
        code = organization.salesorder_code
        objects = SalesOrderModel.objects.last()

        if not objects:  #Check if there are any objects in InoviceModel
            # if there r no objects we should start from the first salesorder number
            previous = 1
            restart = True
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)
        elif (current_date <= dt.datetime.strptime(organization.fiscal_end, '%Y-%m-%d %H:%M:%S')):# if current Date < fiscal end date we generate restart the salesorder number with new prefix
            previous = objects.sales_order_no
            previous = int(previous.split("-")[1])
            restart = False
        else:
            prefixCodeChecker(organization)
            restart = True
            previous = 1
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)

        ### function CAll
        previous = getNewNumber(restart,previous,code)# THIS IS THE SalesOrder NUMBER
        products_data = validated_data.pop('sales_products')    
        print("after asigning")
        validated_data['sales_order_no'] = previous
        salesorder = SalesOrderModel.objects.create(**validated_data)#To get pk of the instance
        for product in products_data:
            SalesProductsModel.objects.create(sales_id = salesorder,**product)
            print("SalesOrder products added")
        return salesorder

    def update(self,instance,validated_data):
        print("inside update method of serializer")
        print('INSTANCE : ',validated_data)
        print()
        nested_data = validated_data.pop('sales_products')
        sales_products = (instance.sales_products).all()
        sales_products = list(sales_products)
        print('INSTANCE of nesteddata : ',nested_data)
        ### updating parent 
        instance.customer_id =  validated_data['customer_id']
        instance.sales_order_status = validated_data['sales_order_status']
        instance.customer_notes = validated_data['customer_notes']
        instance.terms_and_conditions = validated_data['terms_and_conditions']
        instance.adjustment = validated_data['adjustment']
        instance.adjustment_value = validated_data['adjustment_value']
        instance.subtotal = validated_data['subtotal']
        instance.total = validated_data['total']
        instance.save()
        ### updating nested value ###
        if len(nested_data) >= len(sales_products):
            for data in nested_data:
                if len(sales_products) != 0:  
                    sales_product = sales_products.pop(0)
                    print("iter")
                    sales_product.product_id = data.get('product_id')
                    sales_product.quantity= data.get('quantity')
                    sales_product.rate= data.get('rate')
                    sales_product.discount_type= data.get('discount_type')
                    sales_product.discount_value= data.get('discount_value')
                    sales_product.amount= data.get('amount')
                    sales_product.save()
                else:
                    SalesProductsModel.objects.create(sales_id=instance,**data)
        else:
            for i,sales_product in enumerate(sales_products):
                if len(nested_data) > i:
                    sales_product.product_id = nested_data[i].get('product_id')
                    sales_product.quantity= nested_data[i].get('quantity')
                    sales_product.rate= nested_data[i].get('rate')
                    sales_product.discount_type= nested_data[i].get('discount_type')
                    sales_product.discount_value= nested_data[i].get('discount_value')
                    sales_product.amount= nested_data[i].get('amount')
                    sales_product.save()
                else:
                    print(len(nested_data))
                    print('deleting')
                    sales_product.delete()

        return instance 

class PurchaseProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseProductsModel
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    purchase_products = PurchaseProductsSerializer(many=True)
    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'
        read_only_fields = ('purchase_order_no','id')
                
    def create(self, validated_data):
        current_date = dt.datetime.now()
        # current_date = dt.datetime(2021,1,1)
        current_date = dt.datetime(current_date.year, current_date.month, current_date.day)#CREATING A DATE OBJECT
        organization = OrganizationModel.objects.first()
        code = organization.purchaseorder_code
        objects = PurchaseOrderModel.objects.last()

        if not objects:  #Check if there are any objects in InoviceModel
            # if there r no objects we should start from the first purchaseorder number
            previous = 1
            restart = True
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)
        elif (current_date <= dt.datetime.strptime(organization.fiscal_end, '%Y-%m-%d %H:%M:%S')):# if current Date < fiscal end date we generate restart the pruchaseorder number with new prefix
            previous = objects.purchase_order_no
            previous = int(previous.split("-")[1])
            restart = False
        else:
            prefixCodeChecker(organization)
            restart = True
            previous = 1
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)

        ### function CAll
        previous = getNewNumber(restart,previous,code)# THIS IS THE Purchaseorder NUMBER
        products_data = validated_data.pop('purchase_products')    
        print("after asigning")
        validated_data['purchase_order_no'] = previous
        purchaseorder = PurchaseOrderModel.objects.create(**validated_data)#To get pk of the instance
        for product in products_data:
            PurchaseProductsModel.objects.create(purchase_order_id = purchaseorder,**product)
            print("PurchaseOrder products added")
        return purchaseorder

    def update(self,instance,validated_data):
        print("inside update method of serializer")
        # print('INSTANCE : ',validated_data)
        nested_data = validated_data.pop('purchase_products')
        purchase_products = (instance.purchase_products).all()
        purchase_products = list(purchase_products)
        print('INSTANCE : ',nested_data)
        print()
        ###updating parent 
        instance.purchase_order_status = validated_data['purchase_order_status']
        instance.vendor_notes = validated_data['vendor_notes']
        instance.terms_and_conditions = validated_data['terms_and_conditions']
        instance.save()
        ### updating nested value ###
        for data in nested_data:
            purchase_product = purchase_products.pop(0)
            purchase_product.product_id = data.get('product_id')
            purchase_product.purchase_id = data.get('purchase_id')
            purchase_product.quantity= data.get('quantity')
            purchase_product.rate= data.get('rate')
            purchase_product.discount_type= data.get('discount_type')
            purchase_product.discount_value= data.get('discount_value')
            purchase_product.adjustment= data.get('adjustment')
            purchase_product.adjustment_value= data.get('adjustment_value')
            purchase_product.save()
        return instance 

class InvoiceProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProductsModel
        fields = '__all__'
        read_only_fields = ('invoice_id',)

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_products = InvoiceProductsSerializer(many=True)
    class Meta:
        model = InvoiceModel
        fields = '__all__'
        read_only_fields = ('invoice_no',)
                
    def create(self, validated_data):
        current_date = dt.datetime.now()
        # current_date = dt.datetime(2021,1,1)
        current_date = dt.datetime(current_date.year, current_date.month, current_date.day)#CREATING A DATE OBJECT
        organization = OrganizationModel.objects.first()
        code = organization.invoice_code
        objects = InvoiceModel.objects.last()

        if not objects:  #Check if there are any objects in InoviceModel
            # if there r no objects we should start from the first invoice number
            previous = 1
            restart = True
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)
        elif (current_date <= dt.datetime.strptime(organization.fiscal_end, '%Y-%m-%d %H:%M:%S')):# if current Date < fiscal end date we generate restart the invoice number with new prefix
            # invoices_objects = InvoiceModel.objects.order_by('-id')[0]
            previous = objects.invoice_no
            # print("Previous invoice number : ",previous.split("-")[1])
            previous = int(previous.split("-")[1])
            restart = False
        else:
            prefixCodeChecker(organization)
            # if(prefixCodeChecker(organization)==True):
            #     raise serializers.ValidationError('Please Change the Invoice code,Sales code,purchase code')
            
            restart = True
            previous = 1
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)

        ### function CAll
        previous = getNewNumber(restart,previous,code)# THIS IS THE INVOICE NUMBER
        products_data = validated_data.pop('invoice_products')    
        validated_data['invoice_no'] = previous
        invoice = InvoiceModel.objects.create(**validated_data)#To get pk of the instance
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
        read_only_fields = ('date','time','activity_id',)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = '__all__'

    def create(self, validated_data):
        current_date = dt.datetime.now()
        organization = OrganizationModel.objects.create(**validated_data)
        # this is to generate fiscal_end field in ORganization Model
        fiscalDetail(organization,current_date,new=False,instance=None)
        return organization

    def update(self,instance,validated_data):
        print("updating Organization model : ",validated_data['company_name']," instance: ",instance.company_name)
        current_date = dt.datetime.now()
        organization = OrganizationModel.objects.first()
        instance.organization_id = validated_data['organization_id']
        # instance.company_name = validated_data['company_name']
        instance.Phone_number = validated_data['Phone_number']
        instance.email_id= validated_data['email_id']
        instance.salutation= validated_data['salutation']
        instance.first_name= validated_data['first_name']
        instance.last_name= validated_data['last_name']
        instance.invoice_code= validated_data['invoice_code']
        instance.salesorder_code= validated_data['salesorder_code']
        instance.purchaseorder_code= validated_data['purchaseorder_code']
        instance.bill_code= validated_data['bill_code']
        instance.fiscal_detail= validated_data['fiscal_detail']
        instance.fiscal_end = fiscalDetail(organization,current_date,new=True,instance = validated_data['fiscal_detail'])
        # validated_data['fiscal_end'] = fiscal_detail(organization,current_date,new=True)
        # instance.fiscal_end = validated_data['fiscal_end']
        print(instance.fiscal_end)
        instance.save()
        # this is to generate fiscal_end field in Organization Model
        return instance

class BillProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillProductsModel
        fields = '__all__'
        read_only_fields = ('id',)

class BillSerializer(serializers.ModelSerializer):
    bill_products = BillProductsSerializer(many=True)
    class Meta:
        model = BillModel
        fields = '__all__'
        read_only_fields = ('bill_no','id')
                
    def create(self, validated_data):
        current_date = dt.datetime.now()
        # current_date = dt.datetime(2021,1,1)
        current_date = dt.datetime(current_date.year, current_date.month, current_date.day)#CREATING A DATE OBJECT
        organization = OrganizationModel.objects.first()
        code = organization.bill_code
        objects = BillModel.objects.last()

        if not objects:  #Check if there are any objects in InoviceModel
            # if there r no objects we should start from the first bill number
            previous = 1
            restart = True
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)
        elif (current_date <= dt.datetime.strptime(organization.fiscal_end, '%Y-%m-%d %H:%M:%S')):# if current Date < fiscal end date we generate restart the bill number with new prefix
            previous = objects.bill_no
            previous = int(previous.split("-")[1])
            restart = False
        else:
            prefixCodeChecker(organization)
            restart = True
            previous = 1
            last_date_of_fiscal_year = fiscalDetail(organization,current_date,new = True,instance=None)

        ### function CAll
        previous = getNewNumber(restart,previous,code)# THIS IS THE BILL NUMBER
        products_data = validated_data.pop('bill_products')    
        validated_data['bill_no'] = previous
        bill = BillModel.objects.create(**validated_data)#To get pk of the instance
        for product in products_data:
            BillProductsModel.objects.create(bill_id = bill,**product)
            print("Bill products added")
        return bill

    def update(self,instance,validated_data):
        print("inside update method of serializer")
        # print('INSTANCE : ',validated_data)
        nested_data = validated_data.pop('bill_products')
        bill_products = (instance.bill_products).all()
        bill_products = list(bill_products)
        print('INSTANCE : ',nested_data)
        print()
        ###updating parent 
        instance.bill_status = validated_data['bill_status']
        instance.vendor_notes = validated_data['vendor_notes']
        instance.terms_and_conditions = validated_data['terms_and_conditions']
        instance.save()
        ### updating nested value ###
        for data in nested_data:
            bill_product = bill_products.pop(0)
            bill_product.product_id = data.get('product_id')
            bill_product.bill_id = data.get('bill_id')
            bill_product.quantity= data.get('quantity')
            bill_product.rate= data.get('rate')
            bill_product.discount_type= data.get('discount_type')
            bill_product.discount_value= data.get('discount_value')
            bill_product.adjustment= data.get('adjustment')
            bill_product.adjustment_value= data.get('adjustment_value')
            bill_product.save()
        return instance
    

