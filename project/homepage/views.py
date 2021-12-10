from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Menu
from homepage.models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage



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
        
    return render(request,'menu.html',{'products' : productperPage,'category':category_page})

def registerForm(request): 
    return render(request,'register.html')

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
            f = open('file/users.txt', 'r', encoding='utf8')
            s = f.readlines()
            if s != None:
                for line in s:
                  usedEmail = line.split()[2]
                  usedUsername = line.split()[3]
                  
                  if email == usedEmail:
                     checkUser = 1  # emailซำ้
                     break
                  if username == usedUsername:
                     checkUser = 2 # usernameซำ้
                     break
            f.close()      

            if checkUser == 0:
                f = open('file/login.txt', 'a', encoding='utf8')
                f.write(f"{username} {password}\n")
                f.close()

                f = open('file/users.txt', 'a', encoding='utf8')
                f.write(f"{firstname} {lastname} {email} {username} {phone}\n")
                f.close()
                return redirect('/loginForm')
          
            else :
                if checkUser == 1 :
                  messages.info(request,'email ถูกใช้ไปแล้ว')
                elif checkUser == 2 :
                  messages.info(request,'username ถูกใช้ไปแล้ว')
                return redirect('/registerForm')
    
      else :
          messages.info(request,'กรอกข้อมูลไม่ครบ') 
          return redirect('/registerForm')

def loginForm(request):
    return render(request,'login.html')

def login(request):
    if request.method == 'POST':
      # ================= รับข้อมูลจาก form ใน login.html ================= 
      checkLogin = 0
      username = request.POST['username']
      password = request.POST['password']

      # ================= เช็คการกรอกข้อมูล ================= 
      if username != '' and password != '': 

      # ================= เช็คข้อมูลกับไฟล์ login ================= 
        f = open('file/login.txt', 'r', encoding='utf8')
        s = f.readlines()

        if s != None:
          for line in s:
             realUser = line.split()[0]
             realPassword = line.split()[1]
                 
             if username == realUser:
                if password == realPassword:
                    checkLogin = 1
                    break
        f.close()            
        if checkLogin == 1:
            f = open('file/NowLogin.txt', 'w', encoding='utf8')
            f.write("True")
            f.close()
            return render(request,'test.html',
            {
                'checkLogin' : checkLogin,
                'username' : username
            })
        else :
            messages.info(request,'ไม่มีข้อมูลผู้ใช้')
            return redirect('/loginForm')

      else :
         messages.info(request,'กรอกข้อมูลไม่ครบ') 
         return redirect('/loginForm')

    return render(request,'login.html')

def logout(request): 
    return render(request,'index.html',{'checkLogin': 0})

def orderHistory(request):
    return render(request,'orderHistory.html')

def orderInfo(request):
    return render(request,'orderInfo.html')

def cartDetails(request):
    return render(request,'cartDetails.html')

def thanks(request):
    return render(request,'thanks.html')