from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

admin.site.site_header = 'Amnet it solution & engineering'
admin.site.index_title = 'Dashbord'
admin.site.site_title = 'Amnet'

class AllproductAdmin(SummernoteModelAdmin):
# class AllproductAdmin(admin.ModelAdmin):
	list_display = ['name','id','catname','instock','price','quantity']
	list_editable = ['instock','price','quantity']
	summernote_fields = ('fulldetail',)

	# summernote_fields = '__all__'



admin.site.register(Allproduct,AllproductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Category)

class OrderListAdmin(admin.ModelAdmin):
	list_display = ['orderid','productsname','total']



admin.site.register(OrderList,OrderListAdmin)
admin.site.register(OrderPending)
admin.site.register(Contact)
