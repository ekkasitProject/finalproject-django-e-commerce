from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage	
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # register
from django.contrib.auth import authenticate,login 
from datetime import datetime
from django.core.paginator import Paginator #Paginator
# Line noitfy
from songline import Sendline
token ='fE63YpfpcCHEk2owQViN5nMHfcdWrYwZujEi8xgwxhD'
messenger = Sendline(token)






# get =1 
# filer = หลายตัว
# all = ทั้งหมด




def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:4] #ดึงข้อมุลมาจากฐานข้อมุลทั้งหมด
	context = {'product':product}
	return render(request,'myapp/home.html',context)

def About(request):
	return render(request,'myapp/about.html')



def AddContact(request):
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		email = data.get('email')
		detail = data.get('detail')
		

		new = Contact()
		new.name = name
		new.tel = tel
		new.email = email
		new.detail = detail
		new.save()
	
	return render(request,'myapp/contact.html')

def AllContact(request):
	contact = Contact.objects.all().order_by('id').reverse() #ดึงข้อมุลมาจากฐานข้อมุลทั้งหมด
	paginator = Paginator(contact,8) # 1 หน้าโชว์แค่ 8 ชิ้นเท่านั้น
	page = request.GET.get('page')
	contact = paginator.get_page(page)
	context = {'contact':contact}
	return render(request,'myapp/allcontact.html',context)
# 
@login_required	
def AddProduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	category = Category.objects.all()

	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		namedetail = data.get('namedetail')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')
		cat = data.get('category')
		cat = Category.objects.get(catname=cat)

		new = Allproduct()
		new.name = name
		new.namedetail = namedetail
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		new.catname = cat
		###########Save Image############
		try:
			file_image = request.FILES['imageupload']
			file_image_name = request.FILES['imageupload'].name.replace(' ','')
			print('FILE_IMAGE:',file_image)
			print('IMAGE_NAME:',file_image_name)
			fs = FileSystemStorage()
			filename = fs.save(file_image_name,file_image)
			upload_file_url = fs.url(filename)
			new.image = upload_file_url[6:]
		except:
			new.image = '/default.jpg' #หากไม่มีการอัพโหลด จะทำการดึงภาพ default มาใช้งาน
		#######################
		new.save()
	context = {'category':category}
	return render(request, 'myapp/addproduct.html',context)

def Product(request):
	product = Allproduct.objects.all().order_by('id').reverse() #ดึงข้อมุลมาจากฐานข้อมุลทั้งหมด
	paginator = Paginator(product,8) # 1 หน้าโชว์แค่ 8 ชิ้นเท่านั้น
	page = request.GET.get('page')
	product = paginator.get_page(page)
	context = {'product':product}
	return render(request,'myapp/allproduct.html',context)
	# tags
def ProductCategory(request,code):
	selcet =Category.objects.get(id=code)
	product = Allproduct.objects.filter(catname=selcet).order_by('id').reverse() #ดึงข้อมุลมาจากฐานข้อมุลทั้งหมด
	paginator = Paginator(product,8) # 1 หน้าโชว์แค่ 8 ชิ้นเท่านั้น
	page = request.GET.get('page')
	product = paginator.get_page(page)
	context = {'product':product,'catname':selcet.catname}
	return render(request,'myapp/allproductcat.html',context)

def ProductDetail(request,productsid):
	product = Allproduct.objects.get(id=productsid)
	context = {'product':product}
	return render(request,'myapp/productdetail.html',context)


@login_required
def EditProduct(request,productsid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	product = Allproduct.objects.get(id=productsid)
	category = Category.objects.all()

	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		quantity = data.get('quantity')
		unit = data.get('unit')
		cat = data.get('category')
		cat = Category.objects.get(catname=cat)
		instock = data.get('instock')
	# บันทึกลงฐานข้อมูลใหม่
		# product = Allproduct() 
		product.name = name
		product.price = price
		product.detail = detail
		product.quantity = quantity
		product.unit = unit
	########## catname = str ########
		product.catname = cat
	########## 
		if instock == 'instock_true':
			product.instock = True
		else :
			product.instock = False
	######### save image ######
		if 'imageupload' in request.FILES:
			file_image = request.FILES['imageupload']
			file_image_name = request.FILES['imageupload'].name.replace(' ','')
			print('FILE_IMAGE:',file_image)
			print('IMAGE_NAME:',file_image_name)
			fs = FileSystemStorage()
			filename = fs.save(file_image_name,file_image)
			upload_file_url = fs.url(filename)
			product.image = upload_file_url[6:]
		else:
			print('no')
		
		
		product.save()
		
	product = Allproduct.objects.get(id=productsid)
	context = {'product':product,'category':category}

		
	return render(request,'myapp/editproduct.html',context)

def Register(request):
	# เพิ่มลงฐานข้อมูล จากฟอร์ม addproduct.html
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name =last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()
		# from django.contrib.auth import authenticate,login 
		user =authenticate(username=email,password=password)
		login(request,user)
		return redirect('allproduct-page')
	return render(request,'myapp/register.html')

def AddtoCart(request,pid):
	# localhost:800/addtocart/(id)
	# {% url 'addtocart-page' pd.id %}
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		# กรณ๊จำนวนสินค้าซ้ำ
		newcart = Cart.objects.get(user=user,productsid=str(pid))
		newquan =newcart.quantity+1
		newcart.quantity = newquan
		calulate = newcart.price * newquan
		newcart.total = calulate
		newcart.save()

		# update จำนวนของตะกร้าสินค้า ปัจจับัน
		count = Cart.objects.filter(user=user)
		count = sum ([ c.quantity for c in count]) # for loop จำนวนการสั่งซื้อ
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('allproduct-page')
	except:
		newcart = Cart()
		newcart.user = user
		newcart.productsid = pid
		newcart.productsname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calulate = int(check.price) *1
		newcart.total = calulate
		newcart.save()


		# update จำนวนของตะกร้าสินค้า ปัจจับัน
		count = Cart.objects.filter(user=user)
		count = sum ([ c.quantity for c in count]) # for loop จำนวนการสั่งซื้อ
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')


	
def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)

	context = {}

	if request.method == 'POST':
		# ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productsid = data.get('productsid')
		item = Cart.objects.get(user=user,productsid=productsid)
		item.delete()
		context['status'] = 'delete'

		# update จำนวนของตะกร้าสินค้า ปัจจับัน
		count = Cart.objects.filter(user=user)
		count = sum ([ c.quantity for c in count]) # for loop จำนวนการสั่งซื้อ
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		
	mycart = Cart.objects.filter(user=user)
	count = sum ([ c.quantity for c in mycart])
	total = sum ([ c.total for c in mycart])
	context['mycart'] = mycart
	context['count'] = count
	context['total'] = total
	
	return render(request,'myapp/mycart.html',context)

def MyCartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	#แก้ไขจำนวนสินค้า
	if request.method == 'POST':
		data =request.POST.copy()
		# print(data)
		
		if data.get('clear') == 'clear':
			Cart.objects.filter(user=user).delete()
			# update จำนวนของตะกร้าสินค้า ปัจจุบัน
			Cart.objects.filter(user=user)
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
		# k = key , v = value
		editlist = []
		for k,v in data.items():
			# print([k,v])
			if k[:2] == 'pd': #{{pd.productsid}}
				pid = int(k.split('_')[1])
				dt = [pid,int(v)]
				editlist.append(dt)
		# print('EDITLIST:', editlist)
		
		for ed in editlist:
			edit = Cart.objects.get(productsid=ed[0],user=user) #productsid
			edit.quantity = ed[1] #quan
			calulate = edit.price * ed[1]
			edit.total = calulate
			edit.save()

		# update จำนวนของตะกร้าสินค้า ปัจจุบัน
		count = Cart.objects.filter(user=user)
		count = sum ([ c.quantity for c in count]) # for loop จำนวนการสั่งซื้อ
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()


		return redirect('mycart-page')
		# if data.get('checksave') == 'checksave':
		# return redirect('mycart-page')
	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart
	return render(request,'myapp/mycartedit.html',context)

def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		if page == 'submit':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user)
			count = sum ([ c.quantity for c in mycart])
			total = sum ([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total
			return render(request,'myapp/checkout2.html',context)

		if page == 'confirm':
			print('Confirm')
			print(data)
			mycart = Cart.objects.filter(user=user)

			# รหัสคำสั่งซื้อ	
			# id = OD 007 2021 02 15 22 00 31
			mid = str(user.id).zfill(3)
			dt = datetime.now().strftime('%Y%m%d')
			orderid = 'amnet' + mid + dt

			# Line Notify
			productorder = ''
			producttotal = 0


			for pd in mycart:
				order = OrderList()
				order.orderid = orderid
				order.productsid = pd.productsid
				order.productsname = pd.productsname
				order.price = pd.price
				order.quantity = pd.quantity
				order.quantity = pd.quantity
				order.total = pd.total
				order.save() 
			# Line Notify
				productorder = productorder + '- {}\n'.format(pd.productsname) # รายการสินค้า
				producttotal += pd.total
			texttoline = 'amnetID {}\n---\n{}ยอดรวม: {:,.2f} บาท\n ({})'.format(orderid,productorder,producttotal,name)
			# เช็คยอดเพื่อทำสติ๊กเกอร์
			if producttotal > 10000:
				messenger.sticker(102,1,texttoline)
			else:
				messenger.sendtext(texttoline)
			# --------------------- #
			#create order pending
			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()

			# Clear cart
			Cart.objects.filter(user=user).delete()

			# update จำนวนของตะกร้าสินค้า ปัจจุบัน
			Cart.objects.filter(user=user)
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
			# genarate order numbar and save to order Moldes
			# save product in cart to OrderProduct models
			# clear cart
			# redirect to order list page
	return render(request,'myapp/checkout1.html')

def OrderlistPage(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	order = OrderPending.objects.filter(user=user)
	'''
		-order
			-orderid :
			-user :
			-name :
	'''
	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		
		'''
		-odlist
			-object (1)
				-orderid : amnet00xxxxxx
				-products : สินค้าชิ้นที่1
				-total : 500
			-object (2)
				-orderid : amnet00xxxxxx
				-products : สินค้าชิ้นที่2
				-total : 200
			-object (3)
				-orderid : amnet01xxxxxx
				-products : สินค้าชิ้นที่1
		'''

		total = sum ([ c.total for c in odlist])
		# total = sum([500,200])
		od.total = total
		# นับจำนวน order มีจำนวนกี่ชิ้น
		count = sum ([ c.quantity for c in odlist])
		
		if od.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าส่งทั้งหมด (หากเป็นชิ้นแรกคิดค่าส่ง 50บาท ขิ้นถัดไปชิ้นละ 10บาท)
		else:
			shipcost = sum([ 30 if i == 0 else 10 for i in range(count)])
		# เก็บปลายทาง
		if od.shipping == 'cod':
			shipcost += 20 #shipcost =shipcost+20
		od.shipcost = shipcost

	context['allorder'] = order


	return render(request,'myapp/orderlist.html',context)


	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum ([ c.total for c in odlist])
	
	# คำนวนค่าส่งตามประเภทการส่ง
	count = sum ([ c.quantity for c in odlist])
	




# หน้า admin
def AllOrderlistPage(request):
	context = {}

	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum ([ c.total for c in odlist])
		od.total = total

		count = sum ([ c.quantity for c in odlist])
		
		if od.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าส่งทั้งหมด (หากเป็นชิ้นแรกคิดค่าส่ง 50บาท ขิ้นถัดไปชิ้นละ 10บาท)
		else:
			shipcost = sum([ 30 if i == 0 else 10 for i in range(count)])
		# เก็บปลายทาง
		if od.shipping == 'cod':
			shipcost += 20 #shipcost =shipcost+20
		od.shipcost = shipcost

	paginator = Paginator(order,8) # 1 หน้าโชว์แค่ 8 ชิ้นเท่านั้น
	page = request.GET.get('page')
	order = paginator.get_page(page)
	context['allorder'] = order


	return render(request,'myapp/allorderlist.html',context)

def UploadSlip(request,orderid):

	# อัพโหลดสลิป
	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		silptime = data.get('silptime')
		
		update = OrderPending.objects.get(orderid=orderid)
		update.silptime = silptime

		file_image = request.FILES['slip']
		file_image_name = request.FILES['slip'].name.replace(' ','')
		print('FILE_IMAGE:',file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		update.save()


	print('ORDER ID:', orderid)
	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum ([ c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)
	# คำนวนค่าส่งตามประเภทการส่ง
	count = sum ([ c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าส่งทั้งหมด (หากเป็นชิ้นแรกคิดค่าส่ง 50บาท ขิ้นถัดไปชิ้นละ 10บาท)
	else:
		shipcost = sum([ 30 if i == 0 else 10 for i in range(count)])
	# เก็บปลายทาง
	if oddetail.shipping == 'cod':
		shipcost += 20 #shipcost =shipcost+20


	context = {'orderid':orderid,
				'total':total,
				'shipcost':shipcost,
				'grandtotal':total+shipcost,
				'oddetail':oddetail,
				'count':count}


	return render(request,'myapp/uploadsilp.html',context)

def UpdatePaid(request,orderid,status):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	order = OrderPending.objects.get(orderid=orderid)
	if status == 'confirm':
		order.paid = True
		####### ตัดสต๊อก #########
		order.confirmed = True
		odlist = OrderList.objects.filter(orderid=orderid)
		for od in odlist:
			product = Allproduct.objects.get(id=od.productsid)
			product.quantity = product.quantity - od.quantity
			product.save()
		########################
	elif status == 'cancel':
		order.paid = False
		order.confirmed = False
	order.save()
	return redirect('allorderlist-page')

def UpdateTracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		nametracking = data.get('nametracking')
		trackingnumber = data.get('trackingnumber')
		
		order.nametracking = nametracking
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')
		
	context ={'orderid':orderid}
	return render(request,'myapp/updatetracking.html',context)

def MyOrder(request,orderid):
	username = request.user.username
	user = User.objects.get(username=username)
	context ={}

	order = OrderPending.objects.get(orderid=orderid)

	# admin ไม่ได้
	# if user != order.user:
	# 	return redirect('allproduct-page')


	odlist = OrderList.objects.filter(orderid=orderid)

	total = sum ([ c.total for c in odlist])
		# total = sum([500,200])
	order.total = total
		# นับจำนวน order มีจำนวนกี่ชิ้น
	count = sum ([ c.quantity for c in odlist])
		
	if order.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าส่งทั้งหมด (หากเป็นชิ้นแรกคิดค่าส่ง 50บาท ขิ้นถัดไปชิ้นละ 10บาท)
	else:
		shipcost = sum([ 30 if i == 0 else 10 for i in range(count)])
		# เก็บปลายทาง
	if order.shipping == 'cod':
		shipcost += 20 #shipcost =shipcost+20
	order.shipcost = shipcost
	'''
		-odlist
			-object (1)
				-orderid : amnet00xxxxxx
				-products : สินค้าชิ้นที่1
				-total : 500
			-object (2)
				-orderid : amnet00xxxxxx
				-products : สินค้าชิ้นที่2
				-total : 200
			-object (3)
				-orderid : amnet01xxxxxx
				-products : สินค้าชิ้นที่1
		'''
	context ={'order':order,'odlist':odlist,'total':total,'count':count}
	return render(request,'myapp/myorder.html',context)



def PieChart(request):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	products = Allproduct.objects.all()
	order = OrderPending.objects.all()
	pdname = []
	pdquan = []


	for pd in products[:5]:
		pdname.append(pd.name)
		pdquan.append(pd.quantity)

	context	= {'pdname':str(pdname),'pdquan':pdquan,'order':order}
	return render(request,'myapp/graph.html',context)


def Search(request):
	product = Allproduct.objects.filter(name__contains=request.GET['name'])
	context = {'product':product}
	return render(request,'myapp/allproduct.html',context)

def Editprofile(request,username):
	context = {} 
	username = request.user.username #เรียกชื่อผู้ใช้งานหน้าเว็บปัจจุบัน
	user = User.objects.get(username=username) #ดึงข้อมูลผู้ใช้จากชื่อผู้ใช้งานปัจจุบัน
	context['user'] = user #สร้าง context เพื่อนำไปเรียกใช้ใน html
	profile = Profile.objects.get(user=user) #เรียกข้อมูลผู้ใช้จากชื่อผู้ใช้งานปัจจุบัน ในส่วนของ model Profile เพื่อดึง และแก้ไขภาพ
	context['profile'] = profile #สร้าง context เพื่อนำไปเรียกใช้ใน html


	if request.method == 'POST' and request.FILES['photo']:
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		
		user.first_name = first_name
		user.last_name =last_name
		user.save() #สั่งเก็บข้อมูล ชื่อ-สกุล ใหม่
		#จัดการเก็บข้อมูลไฟล์ภาพ โปรไฟล์
		file_image = request.FILES['photo']
		file_image_name = request.FILES['photo'].name.replace(' ','')
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		profile.photo = upload_file_url[6:]
		profile.save() #สั่งเก็บภาพโปรไฟล์ใหม่
		return redirect('home-page') #เมื่อแก้ไขเสร็จให้กลับไปที่หน้า Home 
		

	return render(request,'myapp/editprofile.html',context)

