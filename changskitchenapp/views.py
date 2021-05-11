from django.shortcuts import (get_object_or_404,  render,  HttpResponseRedirect,)
from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DishAddForm
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBTvrZE_ZCXQfCzreRzyxb06OL3cqsx_gE",
    "authDomain": "chang-s-kitchen.firebaseapp.com",
    "databaseURL": "https://chang-s-kitchen-default-rtdb.firebaseio.com",
    "projectId": "chang-s-kitchen",
    "storageBucket": "chang-s-kitchen.appspot.com",
    "messagingSenderId": "5099850523",
    "appId": "1:5099850523:web:c7d4f963145e0463e7a1be",
    "measurementId": "G-19YSNEQ1MY"
    }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
# Create your views here.

def  Home (request):
    return render (request, "home.html")

def  Users (request):
    child = db.child('users').get()
    users = child.val()
    context={
        "users": users,
    }
    return render (request, "users.html",context)

def  Menu (request):
    return render (request, "menu.html")

def  Menu_Manage (request):
    return render (request, "menu_manage.html")

def  Menu_Add (request):
    return render (request, "menu_add.html")


def  Food (request):
    child = db.child('dishes').get()
    dishes = child.val()
    context={
        "dishes": dishes,
    }   
    return render (request, "food.html", context)

def  Order (request):
    child = db.child('orders').get()
    orders = child.val()
    context={
        "orders": orders,
    }
    return render (request, "order.html",context)
    

def Food_Add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DishAddForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/food')
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DishAddForm()

    return render(request, 'food_add.html', {'form': form})



def  Order (request):
    return render (request, "order.html")

def Order_History (request):
    return render (request, "order_history.html")