from django.contrib import admin
from track.models import Product_Track
# Register your models here.


class track(Product_Track):
    class Meta:
        proxy = True



class AnalyticsAdmin(admin.ModelAdmin):
    change_list_template = 'analytics/index.html'
    

admin.site.register(track,AnalyticsAdmin)
