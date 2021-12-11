"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('homepage.urls')),
    path('index/',include('homepage.urls')),
    path('menu/',include('homepage.urls')),

    path('cartdetail/',include('homepage.urls')),

    path('registerForm/',include('homepage.urls')),
    path('addUser',include('homepage.urls')),
    path('loginForm/',include('homepage.urls')),
    path('login',include('homepage.urls')),
    path('logout/',include('homepage.urls')),
    path('orderHistory/',include('homepage.urls')),
    path('orderInfo/',include('homepage.urls')),
    path('thankyou/',include('homepage.urls')),
    path('test/',include('homepage.urls')),
    path('loginHistory/',include('homepage.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

]

