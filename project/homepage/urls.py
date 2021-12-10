from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('',views.index),
  path('index/',views.index),
  path('counter/',views.counter),
  path('menu/',views.menu),
  path('registerForm/',views.registerForm),
  path('addUser',views.addUser),
  path('loginForm/',views.loginForm),
  path('login',views.login),
  path('orderHistory/',views.orderHistory),
  path('orderInfo/',views.orderInfo),
  path('cartDetails/',views.cartDetails),
  path('thanks/',views.thanks),
  path('test/',views.loginForm),
  path('logout/',views.logout)
] 


if settings.DEBUG :
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

