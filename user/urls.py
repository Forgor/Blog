"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from blog.views import blog_list
from .views import logout,login,user_info,register,change_nickname,bond_email,send_vertification_code,change_password,forgot_password


urlpatterns = [
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('user_info/',user_info,name='user_info'),
    path('change_nickname/',change_nickname,name='change_nickname'),
    path('bond_email/',bond_email,name='bond_email'),
    path('logout/',logout,name='logout'),
    path('send_vertification_code/',send_vertification_code,name='send_vertification_code'),
    path('change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

