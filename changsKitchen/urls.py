"""changsKitchen URL Configuration

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
from django.urls import path
from changskitchenapp import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.Home, name='home'),
    path('home/', views.Home, name='home'),
    path('menu/', views.Menu, name='menu'),
    path('menu_add/', views.Menu_Add, name='menu_add'),
    path('food/', views.Food, name='food'),
    path('order/', views.Order, name='order'),
    path('users/', views.Users, name='users'),
    path('food_add/', views.Food_Add, name='food_add'),
    path('food_delete/', views.Food_Delete, name='food_delete'),
    path('food_edit/', views.Food_Edit, name='food_edit'),
    path('search/', views.Search, name ='search'),
    path('searchusers/', views.Searchresults, name = 'search_results'),
    

]
