from django.db import models
from django.contrib.auth.models import User
# Create your models here.

categories = (
   ('VideoGames','videogames'),
   ('ActionFigures','actionfigures'),
   ('Vintage','vintage'),
   ("books","books"),
   ("electronics",'electronics'),
   ("adapter","adapter"),
)

class ProductModel(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=200)
    category = models.CharField(max_length=50,choices=categories, default='VideoGames')
    def __str__(self):
        return str(self.product_name)

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name = "images")
    image = models.ImageField()

class StockModel(models.Model):
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    quantity = models.IntegerField()
    location = models.TextField()

class CustomerModel(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length = 30)
    address = models.TextField()
    phone_no = models.BigIntegerField()
    email = models.EmailField(max_length=254)

class SellModel(models.Model):
    sell_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    customer_id = models.ForeignKey(CustomerModel,blank=True,null = True,on_delete = models.SET_NULL)
    selling_price = models.FloatField()
    sell_date = models.DateField()
    quantity = models.IntegerField()

class BuyModel(models.Model):
    buy_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(ProductModel,on_delete = models.PROTECT)
    customer_id = models.ForeignKey(CustomerModel,blank=True,null=True,on_delete = models.SET_NULL)
    buy_date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    cost_price = models.IntegerField()




