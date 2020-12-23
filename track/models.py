from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True) 

class Product_Track(models.Model):

    counter = models.AutoField(primary_key=True, editable=False)
    merchant_id = models.BigIntegerField()
    user_id = models.CharField(max_length=15,default='null')
    user_email = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_unit = models.PositiveIntegerField(default = 1)
    product_category = models.CharField(max_length=100)
    sku_id = models.CharField(max_length=10)
    mob_no = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now=True,blank=True)
    event = models.CharField(max_length=30,default='product_viewed')
    user_status = models.CharField(max_length=30,default='active')
    order_type = models.CharField(max_length=18,default='Normal Order')
    cartid  = models.CharField(max_length=30)
    product_view_count = models.PositiveIntegerField(default = 0)
    order_total = models.FloatField(default=0)
#https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

class Merchant_Detail(models.Model):

    m_id = models.AutoField(primary_key=True, editable=False)
    merchant_name = models.CharField(max_length=100)
    tracker_id = models.BigIntegerField()
    active = models.BooleanField(default=False)
