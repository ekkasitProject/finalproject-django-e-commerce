from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="photoprofile",null=True,blank=True,default='/default.jpg')
	usertype = models.CharField(max_length=100,default='member')
	cartquan = models.IntegerField(default=0)

	def __str__(self):
		return self.user.first_name

class Category(models.Model):
	catname = models.CharField(max_length=200,default='สินค้าทั่วไป')
	detail = models.TextField(null=True,blank=True)
	def __str__(self):
		return self.catname
		
class Allproduct(models.Model):
	catname = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
	name = models.CharField(max_length=100)
	namedetail = models.CharField(max_length=100,null=True,blank=True)
	price = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True)
	instock = models.BooleanField(default=True)
	unit = models.CharField(max_length=200,default='-')
	quantity = models.IntegerField(default=1)
	image = models.ImageField(upload_to="products",null=True,blank=True)


	# คู่มือสินค้า
	fulldetail = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.name
	
class Contact(models.Model):
	name = models.CharField(max_length=100)
	tel = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	detail = models.TextField(null=True,blank=True)
	def __str__(self):
		return self.name


class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	productsid = models.CharField(max_length=100)
	productsname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()
	stemp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	
class OrderList(models.Model):
	orderid = models.CharField(max_length=100)
	productsid = models.CharField(max_length=100)
	productsname = models.CharField(max_length=100)
	price = models.IntegerField()
	quantity = models.IntegerField()
	total = models.IntegerField()

class OrderPending(models.Model):
	orderid = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	tel = models.CharField(max_length=100)
	address = models.TextField()
	shipping = models.CharField(max_length=100)
	payment = models.CharField(max_length=100) 
	other = models.TextField(blank=True,null=True)
	stemp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	# จ่ายเงินหรือยัง
	paid = models.BooleanField(default=False)
	confirmed = models.BooleanField(default=False)
	slip = models.ImageField(upload_to="slip",null=True,blank=True)
	silptime = models.CharField(max_length=100,null=True,blank=True) #มาเพิ่มประเภท datetime พร้อมกับ calender html
	paymentid = models.CharField(max_length=100,null=True,blank=True) 
	nametracking = models.CharField(max_length=100,null=True,blank=True) 
	trackingnumber = models.CharField(max_length=100,null=True,blank=True) 
	def __str__(self):
		return self.orderid