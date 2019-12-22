import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventory_management.settings')
import random
import django
django.setup()

from Inventory_rest_api.models import ProductModel,ProductGroupModel,VendorModel,CustomerModel
from faker import Faker
from django.core import serializers





obj = Faker()
def vendor(N):
    for _ in range(N):
        c1 = "mr"
        c2 = obj.name()
        c3 = obj.random.randint(9000000000,9999999999)
        c4 = obj.email()
        c5 = obj.paragraph()
        # print(c3)
        vendor_obj = VendorModel.objects.get_or_create(salutation = c1,vendor_name = c2,vendor_phno = c3,vendor_email = c4,remarks = c5)
    print('vendor has been populated')

def customer(N):
    for _ in range(N):
        c1 = "mr"
        c2 = obj.name()
        c3 = obj.random.randint(9000000000,9999999999)
        c4 = obj.email()
        c5 = obj.paragraph()
        c6 = obj.random.randint(1000,9999)
        # print(c3)
        customer_obj = CustomerModel.objects.get_or_create(salutation = c1,customer_name = c2,phone_no = c3,email = c4,remarks = c5,outstanding_recievables=c6)
        print(customer_obj)


def productGroup(N):
    UNIT_CHOICES = [('box', 'box'),
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
    arr = [
        'furniture','stationary','woods','automobile','computer','smartphones','handheld','games','video','audio'
    ]
    arr[0]
    for i in range(N):
        c1 = arr[i]
        c2 = UNIT_CHOICES[i][0]
        c3 = 'color'
        c4 = obj.color_name()
        group_obj = ProductGroupModel.objects.get_or_create(group_name = c1,unit = c2,attribute = c3,value = c4)
    print("added")


def products(N):
    arr = [
        'Mouse','Keyboard','Monitor','Cpu','gpu','ups','car','motor','pendrive','pencil',
    ]
    group_names = ProductGroupModel.objects.values('group_name')
    print(type(group_names))
    group_names = serializers.serialize("json", group_names)
    print(group_names)
    # for i in range(N):
    #     c1 = arr[i]
    #     c2 = obj.paragraph()
    #     c3 = group_names[i]
    #     product_obj = ProductModel.objects.get_or_create(product_name = c1,product_description = c2,group_id = c3)

    print('added')


customer(10)
# vendor(10)
# productGroup(10)
# products(10)