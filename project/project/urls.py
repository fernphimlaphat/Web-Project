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
from homepage import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin', admin.site.urls),
    path('',include('homepage.urls')),
    path('index/',include('homepage.urls')),
    path('menu/',include('homepage.urls')),
    path('',views.menu,name="AllMenu"),
    path('category/<slug:category_slug>',views.menu,name="product_by_category"),
    path('registerForm/',include('homepage.urls')),
    path('addUser',include('homepage.urls')),
    path('loginForm/',include('homepage.urls')),
    path('login',include('homepage.urls')),
    path('logout/',include('homepage.urls')),
    path('orderHistory/',include('homepage.urls')),
    path('orderInfo/',include('homepage.urls')),
    path('cartDetails/',include('homepage.urls')),
    path('thanks/',include('homepage.urls')),
    path('test/',include('homepage.urls')),

]

if settings.DEBUG :
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)

