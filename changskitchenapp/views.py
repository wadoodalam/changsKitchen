
from typing_extensions import ParamSpec
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
    data = db.child('users').shallow().get().val()
    orderslist = []
    comb_list = []
    # append all the id in uidlist
    for i in data:
        orderslist.append(i)
    Email = [] 
    Password = []
    Name = []
    Phone = []
    Uid = []
    for i in orderslist:

        email = db.child('users').child(i).child('email').get().val()
        name = db.child('users').child(i).child('name').get().val()
        password = db.child('users').child(i).child('password').get().val()
        phone = str(db.child('users').child(i).child('phone').get().val())
        uid = db.child('users').child(i).child('uid').get().val()

        Email.append(email)
        Name.append(name)
        Password.append(password)
        Phone.append(phone)
        Uid.append(uid)

        # the list contains the description, name and price of all dishes.
        
        comb_list = Email + Name + Password + Phone + Uid
    
    context={
        "comb_list": comb_list,
    }
    return render (request, "users.html",context)

def  Menu (request):
    return render (request, "menu.html")

def  Menu_Manage (request):
    return render (request, "menu_manage.html")

def  Menu_Add (request):
    return render (request, "menu_add.html")


def  Food (request):
    data = db.child('dishes').shallow().get().val()
    orderslist = []
    comb_list = []
    # append all the id in uidlist
    for i in data:
        orderslist.append(i)
    Description = [] 
    Name = []
    Price = []
    for i in orderslist:

        description = db.child('dishes').child(i).child('description').get().val()
        name = db.child('dishes').child(i).child('name').get().val()
        price = str(db.child('dishes').child(i).child('price').get().val())
        
        Description.append(description)
        Name.append(name)
        Price.append(price)
        # the list contains the description, name and price of all dishes.
        # example output for comb_list = [None, None, 'none1', 'chicken 65', '0.0', '12.0']
        comb_list = Description+Name+Price
    
    context={
        "comb_list": comb_list,
    }
    return render (request, "food.html", context)

def  Order (request):
    data = db.child('orders').shallow().get().val()
    orderslist = []
    comb_list = []
    # append all the id in uidlist
    for i in data:
        orderslist.append(i)
    Date = [] 
    FinalPrice = []
    Items = []
    Status = []
    StringDate = []
    Summary = []
    Cost = []
    Tax = []
    Tip = []
    Uid = []
    for i in orderslist:

        date = db.child('orders').child(i).child('date').get().val()
        finalPrice = str(db.child('orders').child(i).child('finalPrice').get().val())
        items = db.child('orders').child(i).child('items').get().val()
        status = db.child('orders').child(i).child('status').get().val()
        stringDate = db.child('orders').child(i).child('stringDate').get().val()
        summary = db.child('orders').child(i).child('summary').get().val()
        cost = str(db.child('orders').child(i).child('cost').get().val())
        tax = str(db.child('orders').child(i).child('tax').get().val())
        tip = str(db.child('orders').child(i).child('tip').get().val())
        uid = db.child('orders').child(i).child('uid').get().val()

        Date.append(date)
        FinalPrice.append(finalPrice)
        Items.append(items)
        Status.append(status)
        StringDate.append(stringDate)
        Summary.append(summary)
        Cost.append(cost)
        Tax.append(tax)
        Tip.append(tip)
        Uid.append(uid)
        # the list contains the properties or orders
        comb_list = Date + FinalPrice +  Items +Status + StringDate + Summary + Cost + Tax + Tip + Uid 
    
    context={
        "comb_list": comb_list,
    }

    return render (request, "order.html", context)
    

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
