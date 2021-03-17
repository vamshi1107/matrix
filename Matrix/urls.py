"""Matrix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .view import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',login,name="login"),
    path("",index,name="index"),
    path('profile', profile, name="profile"),
    path('register', register, name="register"),
    path('newuser', new_user, name="register"),
    path('logout', logout, name="logout"),
    path('json',user_data,name="json"),
    path('search', search, name="search"),
    path('req', send_request, name="request"),
    path('remove', remove, name="remove"),
    path('userfriends/<str:user>', show_friends, name="showfriends"),
    path('remreq', remove_request, name="remreq"),
    path('add', add_friend, name="add"),
    path('friends', friends, name="friends"),
    path('post', newpost, name="post"),
    path('addpic', add_pic, name="addpic"),
    path('check/<str:user>', check, name="post"),
    path('removepost/<int:id>', remove_post, name="rem"),
    path('user/<str:user>', userpage, name="json"),

]
