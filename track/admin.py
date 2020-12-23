from django.contrib import admin
from .models import Product_Track,Merchant_Detail,UserProfile
# Register your models here.
class Product_TrackAdmin(admin.ModelAdmin):
    list_display = ['counter','merchant_id','cartid','user_id','user_email','mob_no','sku_id','product_category','product_name','product_price','product_unit','order_type', 'order_total','product_view_count','timestamp','user_status','event']
    list_filter = ['product_category','timestamp','event','user_status']
    search_fields = ['user_id','product_name','user_email']

admin.site.register(Product_Track, Product_TrackAdmin)


class Merchant_DetailAdmin(admin.ModelAdmin):
    list_display = ['m_id','merchant_name','tracker_id','active']
    list_filter = ['active']
    search_fields = ['m_id','merchant_name']


admin.site.register(Merchant_Detail, Merchant_DetailAdmin)

class UserProfile_DetailAdmin(admin.ModelAdmin):
    list_display = ['user','mobile']
    search_fields = ['user']


admin.site.register(UserProfile, UserProfile_DetailAdmin)
