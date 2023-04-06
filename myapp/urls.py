from django.urls import path,include 
from .views import *

urlpatterns = [
    path('',Home,name='home-page'),
    path('about/',About,name='about-page'),
    path('contact/',AddContact,name='contact-page'),
    path('allcontact/',AllContact,name='allcontact-page'),
    path('addproduct/',AddProduct,name='addproduct-page'),
    path('allproduct/',Product,name='allproduct-page'),
    path('register/',Register,name='register-page'),
    path('addtoCart/<int:pid>',AddtoCart,name='addtocart-page'),
    path('mycart/',MyCart,name='mycart-page'),
    path('mycartedit/',MyCartEdit,name='mycartedit-page'),
    path('checkout/',Checkout,name='checkout-page'),
    path('orderlist/',OrderlistPage,name='orderlist-page'),
    path('allorderlist/',AllOrderlistPage,name='allorderlist-page'),
    path('uploadsilp/<str:orderid>',UploadSlip,name='uploadsilp-page'),
    path('updatestatus/<str:orderid>/<str:status>',UpdatePaid,name='updatestatus'),
    path('updatetracking/<str:orderid>/',UpdateTracking,name='updatetracking'),
    path('myorder/<str:orderid>/',MyOrder,name='myorder-page'),
    path('graph/',PieChart,name='graph-page'),
    path('product/<int:productsid>/',ProductDetail,name='detail-page'),
    path('editproduct/<int:productsid>/',EditProduct,name='editproduct-page'),
    #tags 
    path('category/<int:code>',ProductCategory,name='category-page'),
    path('search/',Search,name='search-page'),

    
    path('editprofile/<str:username>/',Editprofile, name='editprofile-page'),
]
