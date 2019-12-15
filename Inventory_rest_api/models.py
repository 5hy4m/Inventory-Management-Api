from django.db import models
from django.contrib.auth.models import User
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

SALUTATION_CHOICES = [
    ('mr','mr'),
    ('mrs','mrs'),
    ('ms','ms'),
    ('miss','miss'),
    ('dr','dr'),
]

class ProductGroupModel(models.Model):
    group_id = models.AutoField(primary_key = True)
    group_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=3,choices=UNIT_CHOICES,)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=50,default = "")
    def __str__(self):
        return self.group_name

class ProductModel(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=200)
    group_id = models.ForeignKey(ProductGroupModel,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.product_name)

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name = "images")
    image = models.ImageField()

    def __str__(self):
        return self.product

class StockModel(models.Model):
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    quantity = models.IntegerField()
    location = models.TextField()

    def __str__(self):
        return self.product_id

class CustomerModel(models.Model):
    customer_id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length = 4,choices = SALUTATION_CHOICES)
    customer_name = models.CharField(max_length = 30)
    phone_no = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    remarks = models.TextField() #Remarks Are for Internal Use only

    def __str__(self):
        return self.customer_name

class CustomerAddressModel(models.Model):
    customer_address_id = models.ForeignKey(CustomerModel,on_delete = models.CASCADE)
    country = models.CharField(max_length = 50)
    zipcode = models.BigIntegerField()
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    street = models.CharField(max_length = 50)

class VendorModel(models.Model):
    vendor_id = models.AutoField(primary_key = True)
    vendor_name = models.CharField(max_length = 50)
    vendor_email = models.CharField(max_length = 50)
    vendor_phno = models.BigIntegerField()
    salutation = models.CharField(max_length = 4,choices = SALUTATION_CHOICES)
    remarks = models.TextField()

    def __str__(self):
        return self.vendor_name

class VendorAddressModel(models.Model):
    vendor_address_id = models.ForeignKey(VendorModel,on_delete = models.CASCADE)
    country = models.CharField(max_length = 50)
    zipcode = models.BigIntegerField()
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    street = models.CharField(max_length = 50)

class SaleModel(models.Model):
    sale_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    customer_id = models.ForeignKey(CustomerModel,blank=True,null = True,on_delete = models.SET_NULL)
    selling_price = models.FloatField()
    sale_date = models.DateField()
    quantity = models.IntegerField()

class SalesOrderModel(models.Model):
    sale_order_no = models.AutoField(primary_key=True)
    sale_id = models.ForeignKey(SaleModel,on_delete = models.CASCADE)
    customer_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):
        return sale_order_no

class PurchaseModel(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    customer_id = models.ForeignKey(CustomerModel,blank=True,null=True,on_delete = models.SET_NULL)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    cost_price = models.IntegerField()

class PurchaseOrderModel(models.Model):
    purchase_order_no = models.AutoField(primary_key=True)
    purchase_id = models.ForeignKey(PurchaseModel,on_delete = models.CASCADE)
    customer_notes = models.TextField()
    terms_and_conditions = models.TextField()

class InvoiceModel(models.Model):
    invoice_no = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(PurchaseModel,on_delete = models.PROTECT)
    invoice_date = models.DateField()
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    due_date = models.DateField()
    customer_notes = models.TextField()
    terms_and_conditions = models.TextField()

    def __str__(self):
        return self.invoice_no

class ActivitiesModel(models.Model):
    activity_id = models.AutoField(primary_key=True)
    ids = models.IntegerField()
    activity_name = models.CharField(max_length = 250)
    date = models.DateField()
    timestamp = models.CharField(max_length = 250,default = "")