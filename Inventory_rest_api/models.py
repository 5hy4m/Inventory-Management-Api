from django.db import models
from django.contrib.auth.models import User
import datetime as dt
# Create your models here.

UNIT_CHOICES = [
    ('box', 'box'),
    ('cm', 'cm'),
    ('dz', 'dz'),
    ('ft', 'ft'),
    ('g', 'g'),
    ('kg', 'kg'),
    ('km', 'km'),
    ('lg', 'lg'),
    ('mg', 'mg'),
    ('m', 'm'),
    ('pcs', 'pcs'),
]

DISCOUNT_CHOICES = [
    ('',''),
    ("rs","rs"),
    ('%','%'),
]

SALUTATION_CHOICES = [
    ('mr','mr'),
    ('mrs','mrs'),
    ('ms','ms'),
    ('miss','miss'),
    ('dr','dr'),
]

FISCAL_YEAR = [
    ("1-12","jan-dec"),
    ("2-1","feb-jan"),
    ("3-2","mar-feb"),
    ("4-3","apr-mar"),
    ("5-4","may-apr"),
    ("6-5","jun-may"),
    ("7-6","jul-jun"),
    ("8-7","aug-jul"),
    ("9-8","sep-aug"),
    ("10-9","oct-sep"),
    ("9-10","nov-oct"),
    ("12-11","dec-nov")
    ]

ADJUSTMENT_CHOICES = [
        ('',''),
        ('+','+'),
        ('-','-'),
    ]

INVOICE_STATUS=[
    ("draft",'draft'),
    ('unpaid','unpaid'),
    ('paid','paid')
    ]

BILL_STATUS=[
    ("draft",'draft'),
    ('unpaid','unpaid'),
    ('paid','paid')
    ]

SALES_ORDER_STAUS = [
    ("draft",'draft'),
    ("confirmed",'confirmed'),
    ("delivered",'delivered'),
    ]

PURCHASE_ORDER_STATUS = [
    ("draft",'draft'),
    ("issued",'issued'),
    ("confirmed",'confirmed')
    ]

ADDRESS_TYPE = [
    ('customer','customer'),
    ('vendor','vendor'),
    ('organization','organization'),
]

class CustomerModel(models.Model):
    customer_id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length = 4,choices = SALUTATION_CHOICES)
    customer_name = models.CharField(max_length = 30)
    phone_no = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    remarks = models.TextField() #Remarks Are for Internal Use only
    recievables = models.IntegerField( default=0) 

    def __str__(self):
        return self.customer_name

class ProductGroupModel(models.Model):
    group_id = models.AutoField(primary_key = True)
    group_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=3,choices=UNIT_CHOICES,)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=50,default = "")
    def __str__(self):
        return self.group_name

class ProductModel(models.Model):
    group_id = models.ForeignKey(ProductGroupModel,blank=True, null=True,on_delete=models.CASCADE) 
    product_id = models.AutoField(blank=True,primary_key=True)
    product_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=3,choices=UNIT_CHOICES,default = UNIT_CHOICES[-1][0])
    product_description = models.TextField(max_length=200)
    selling_price = models.FloatField(default=0)
    cost_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.product_id)

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name = "images")
    image = models.ImageField()

    def __str__(self):
        return self.product

class StockModel(models.Model):
    product_id = models.OneToOneField(ProductModel,related_name="stocks",on_delete = models.CASCADE,blank=True)
    quantity = models.FloatField()
    location = models.TextField(blank=True,null=True)
    commited = models.FloatField(default=0)
    def __str__(self):
        return str(self.product_id)

class VendorModel(models.Model):
    vendor_id = models.AutoField(primary_key = True)
    vendor_name = models.CharField(max_length = 50)
    vendor_email = models.CharField(max_length = 50)
    vendor_phno = models.BigIntegerField()
    salutation = models.CharField(max_length = 4,choices = SALUTATION_CHOICES)
    remarks = models.TextField()
    payables = models.IntegerField(default=0)
    def __str__(self):
        return self.vendor_name

class BillModel(models.Model):
    bill_no = models.CharField(max_length=10,unique=True)
    bill_date = models.DateField(auto_now_add=True)
    bill_time = models.TimeField(auto_now_add=True)
    due_date = models.DateField()
    bill_status = models.CharField(max_length=10,choices=BILL_STATUS,default=BILL_STATUS[0][0])
    vendor_id = models.ForeignKey(VendorModel,blank=True,null=True,on_delete = models.PROTECT)
    vendor_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):
        return str(self.bill_no)

class BillProductsModel(models.Model):
    bill_id = models.ForeignKey(BillModel,related_name='bill_products',blank=True,on_delete = models.CASCADE)
    product_id = models.ForeignKey(ProductModel,on_delete = models.SET_NULL,blank=True,null=True)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount_type = models.CharField(max_length = 3,choices = DISCOUNT_CHOICES)
    discount_value = models.FloatField()
    adjustment = models.CharField(max_length=3,choices = ADJUSTMENT_CHOICES)
    adjustment_value = models.FloatField()

    def __str__(self):
        return str(self.bill_id)

class InvoiceModel(models.Model):
    invoice_no = models.CharField(max_length=10,unique=True)
    customer_id = models.ForeignKey(CustomerModel,on_delete = models.PROTECT)
    invoice_date = models.DateField(auto_now_add=True)
    invoice_time = models.TimeField(auto_now_add=True)
    due_date = models.DateField()
    invoice_status = models.CharField(max_length=10,choices = INVOICE_STATUS,default=INVOICE_STATUS[0][0])
    customer_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):
        return str(self.invoice_no)

class InvoiceProductsModel(models.Model):
    invoice_id = models.ForeignKey(InvoiceModel,related_name='invoice_products',blank=True,on_delete = models.CASCADE)
    product_id = models.ForeignKey(ProductModel,on_delete = models.SET_NULL,blank=True,null=True)
    quantity = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    discount_type = models.CharField(max_length = 3,choices = DISCOUNT_CHOICES,default=DISCOUNT_CHOICES[0][0])
    discount_value = models.FloatField(default=0)
    adjustment = models.CharField(max_length=3,choices = ADJUSTMENT_CHOICES,default=ADJUSTMENT_CHOICES[0][0])
    adjustment_value = models.FloatField(default = 0)

    def __str__(self):  
        return str(self.invoice_id)

class PurchaseOrderModel(models.Model):
    purchase_order_no = models.CharField(max_length=10,unique=True)
    purchase_date = models.DateField(auto_now_add=True)
    purchase_time = models.TimeField(auto_now_add=True)
    purchase_order_status = models.CharField(max_length=10,choices=PURCHASE_ORDER_STATUS,default=PURCHASE_ORDER_STATUS[0][0])
    vendor_id = models.ForeignKey(VendorModel,blank=True,null=True,on_delete = models.PROTECT)
    vendor_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):  
        return str(self.purchase_order_no)

class PurchaseProductsModel(models.Model):
    purchase_order_id = models.ForeignKey(PurchaseOrderModel,related_name='purchase_products',blank=True,on_delete = models.CASCADE)
    product_id = models.ForeignKey(ProductModel,on_delete = models.SET_NULL,blank=True,null=True)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount_type = models.CharField(max_length = 3,choices = DISCOUNT_CHOICES)
    discount_value = models.FloatField()
    adjustment = models.CharField(max_length=3,choices = ADJUSTMENT_CHOICES)
    adjustment_value = models.FloatField()

    def __str__(self):  
        return str(self.purchase_order_id)

class SalesOrderModel(models.Model):
    # sale_id = models.AutoField(primary_key=True)
    sales_order_no = models.CharField(max_length=10,unique=True)
    sales_order_status = models.CharField(max_length=10,default=SALES_ORDER_STAUS[0][0],choices = SALES_ORDER_STAUS)
    sales_order_date = models.DateField(auto_now_add=True)
    sales_order_time = models.TimeField(auto_now_add=True)
    customer_id = models.ForeignKey(CustomerModel,blank=True,null = True,on_delete = models.PROTECT)
    customer_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):
        return self.sales_order_no

class SalesProductsModel(models.Model):
    sales_id = models.ForeignKey(SalesOrderModel,related_name='sales_products',blank=True,on_delete = models.CASCADE)
    product_id = models.ForeignKey(ProductModel,on_delete = models.SET_NULL,blank=True,null=True)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount_type = models.CharField(max_length = 3,choices = DISCOUNT_CHOICES)
    discount_value = models.FloatField()
    adjustment = models.CharField(max_length=3,choices = ADJUSTMENT_CHOICES)
    adjustment_value = models.FloatField()

class ActivityModel(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    ids = models.CharField(max_length=15,null = False)
    activity_name = models.CharField(max_length = 250)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    description = models.TextField(max_length=300,default="")
    
    def __str__(self):
        return self.activity_name
    # timestamp = models.DateField(auto_now_add=True)

class OrganizationModel(models.Model):
    organization_id = models.IntegerField(primary_key=True,blank=True,default=1)
    company_name = models.CharField(max_length=50)
    Phone_number = models.BigIntegerField(null=True)
    email_id = models.EmailField()
    salutation = models.CharField(max_length=4,choices=SALUTATION_CHOICES)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    invoice_code = models.CharField(max_length=5)
    salesorder_code = models.CharField(max_length=5)
    purchaseorder_code = models.CharField(max_length=5)
    bill_code = models.CharField(max_length=5,default = 'Bill-')
    fiscal_detail = models.CharField(max_length = 8,choices = FISCAL_YEAR)
    fiscal_end = models.CharField(max_length = 50,blank=True,default = "")

    def __str__(self):
        return self.company_name

class AddressModel(models.Model):
    # address_id = models.ForeignKey(OrganizationModel,on_delete = models.CASCADE)
    ids = models.IntegerField()
    address_type = models.CharField(max_length=20,choices = ADDRESS_TYPE,default=ADDRESS_TYPE[0][0])
    country = models.CharField(max_length = 50)
    zipcode = models.BigIntegerField()
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    street = models.CharField(max_length = 50)
