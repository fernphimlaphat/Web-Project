from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Menu
from homepage.models import Category,Product,Cart,CartItem
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required



#================= Class ================= 
class Stack:
    def __init__(self,lst = None):
        self.lst = lst if lst is not None else []
    def push(self,item):
        self.lst.append(item)
    def pop(self):
        self.lst.pop()
    def peek(self):
        return self.lst[-1]
    def size(self):
        return len(self.lst)
    def isEmpty(self):
        return len(self.lst) == 0
    def show(self):
        return self.lst
    def find(self,num):
        return self.lst[num]    

class Queue:
    def __init__(self,lst = None):
        self.lst = lst if lst is not None else []
    def size(self):
        return len(self.lst)
    def isEmpty(self):
        return len(self.lst) == 0
    def top(self):
        return self.lst[0]
    def enqueue(self,obj):
        self.lst.append(obj)
    def dequeue(self):
        return self.lst.pop(0)
    def show(self):
        return self.lst

class sorting:
    pass
#================= END Class ================= 



#================= การทำงาน ================= 

# Create your views here.
def index(request):
    return render(request,'index.html')

def counter(request):
    text = request.POST['text']
    amount_of_text = len(text.split())
    return render(request,'counter.html',{'count': amount_of_text})

def menu(request,category_slug=None):
    products = None
    category_page=None

    if category_slug != None:
        category_page = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.all().filter(category=category_page,available=True)
    else:
        products = Product.objects.all().filter(available=True)
    
    #n / 12 = หน้า
    paginator=Paginator(products,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        productperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage=paginator.page(paginator.num_pages)
        
    return render(request,'menu.html',{'products' : productperPage,'category':category_page ,})

#id สินค้า เพื่อตัวแปรในการส่งข้อมูล
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

@login_required(login_url='/loginForm')
def addCart(request,product_id):
    #ดึงสินค้าที่เราซื้อมาใช้งาน
    product=Product.objects.get(id=product_id)
    ################################## สร้างตะกร้าสินค้า #####################################

    #สร้างตะกร้าแล้ว
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    #ยังไม่สร้างตะกร้า
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
     
    #ซื้อรายการสินค้าซ้ำ
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock :
            #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity+=1
            #บันทึก/อัพเดทค่า
            cart_item.save()
    
    #ซื้อรายการสินค้าครั้งแรก
    #บันทึกลงฐานข้อมูล
    except CartItem.DoesNotExist:  
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('cartdetail')

def removeCart(request,product_id):
    #ทำงานกับตะกร้าสินค้า id นั้นๆ
    cart=Cart.objects.get(cart_id=_cart_id(request))
    #ทำงานกับสินค้าที่จะลบ
    product=get_object_or_404(Product,id=product_id)
    cartItem=CartItem.objects.get(product=product,cart=cart)
    #ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า (CartItem)
    cartItem.delete()
    return redirect('cartdetail')

def cartdetail(request):
    total=0
    counter=0
    TimeCook=0
    Hour=0
    Min=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=item.quantity
            TimeCook+=item.product.TimeCook
            Hour=TimeCook//60
            Min=TimeCook%60

    except Exception as e :
        pass

    return render(request,'cartdetail.html',
    dict(cart_items=cart_items,total=total,counter=counter,TimeCook=TimeCook,Hour=Hour,Min=Min
    ))

def registerForm(request): 
    return render(request,'register.html')

def orderHistory(request):
    return render(request,'orderHistory.html')

def orderInfo(request):
    return render(request,'orderInfo.html')

def cartDetails(request):
    return render(request,'cartDetails.html')

def thanks(request):

    return render(request,'thanks.html')

def search(request):
    products=Product.objects.filter(name__contains=request.GET['title'])
    return render(request,'menu.html',{'products':products})

def addUser(request): 
    if request.method == 'POST':
      checkUser = 0
      # ================= รับข้อมูลจาก form ใน register.html ================= 
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      email = request.POST['email']
      username = request.POST['username']
      phone = request.POST['phone']
      password = request.POST['password']
      
      # ================= เช็คการกรอกข้อมูล ================= 
      if firstname != '' and lastname != '' and email != '' and username != '' and phone != '' and password != '' : 

            # ================= เช็คข้อมูลกับไฟล์ Users ================= 
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username มีคนใช้แล้ว')
                return redirect('/registerForm')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email มีคนใช้แล้ว')
                return redirect('/registerForm')
            user=User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname
            )
            user.save()
            return redirect('/loginForm')
    
      else :
          messages.info(request,'กรอกข้อมูลไม่ครบ') 
          return redirect('/registerForm')

def loginForm(request):
    return render(request,'login.html')

def login(request):
    if request.method == 'POST':
      # ================= รับข้อมูลจาก form ใน login.html ================= 
      username = request.POST['username']
      password = request.POST['password']
      
      # ================= เช็คการกรอกข้อมูล ================= 
      if username != ''and password != '' : 
          
        # ================= เช็ค login ================= 
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'ไม่พบข้อมูล')  
            return redirect('/loginForm')
        
    
      else :
         messages.info(request,'กรอกข้อมูลไม่ครบ') 
         return redirect('/loginForm')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
