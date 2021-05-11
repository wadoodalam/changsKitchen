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
    for i in orderslist:

        description = db.child('dishes').child(i).child('description').get().val()
        name = db.child('dishes').child(i).child('name').get().val()
        price = str(db.child('dishes').child(i).child('price').get().val())
        
        food = {
            "description": description,
            "name": name,
            "price": price
        }
        # the list contains the description, name and price of all dishes.
        # example output for comb_list = [None, None, 'none1', 'chicken 65', '0.0', '12.0']
        comb_list.append(food)
    
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

        order = {
            "date": date,
            "finalPrice": finalPrice,
            "items": items,
            "status": status,
            "stringDate": stringDate,
            "summary": summary,
            "cost": cost,
            "tax": tax,
            "tip": tip,
            "uid": uid
        }
        comb_list.append(order)
    
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

def Search (request):
    return render (request, "search.html")

def Searchusers(request):
    value = request.POST.get('search')
      
    # if no value is given then render to search.h6tml
    if value =="":
        return render(request, "search.html")
    title = request.POST['category']
    if title =="":
        return render(request, "search.html")
    if value is None or title is None:
        return render(request, "search.html")
    else:
        if title == "Users":

            data = db.child('users').shallow().get().val()
            uidlist = []
            requid = 'null'
            
            # append all the id in uidlist
            for i in data:
                uidlist.append(i)
                
            # if we have find all the uid then
            # we will look for the one we need    
            for i in uidlist:
                val = db.child('users').child(i).child('name').get().val()
                val1 = db.child('users').child(i).child('email').get().val()
                val2 = db.child('users').child(i).child('phone').get().val()
                val=val.lower()
                val1=val1.lower()
                val2=val2.lower()
                value=value.lower()
                # if uid we want is value then
                # we will store that in requid
                if (val == value or val1 == value or val2 == value ) :
                    requid = i
            if requid=='null':
                return render(request, "search.html")
            
            # then we will retrieve all the data related to that uid
            email = db.child('users').child(requid).child('email').get().val()
            name = db.child('users').child(requid).child('name').get().val()
            phone = str(db.child('users').child(requid).child('phone').get().val())
            uid = db.child('users').child(requid).child('uid').get().val()

            Name = []
            Name.append(name)
            Email = []
            Email.append(email)
            Phone = []
            Phone.append(phone)
            Uid = []
            Uid.append(uid)
            comb_lis = zip(Email, Name, Phone, Uid)
            
            # send all data in zip form to searchusers.html
            return render(request, "searchusers.html", {"comb_lis": comb_lis})
        elif title == "Dishes":
            data = db.child('dishes').shallow().get().val()
            uidlist = []
            requid = 'null'
              
            # append all the id in uidlist
            for i in data:
                uidlist.append(i)
                  
            # if we have find all the uid then
            # we will look for the one we need    
            for i in uidlist:
                val = db.child('dishes').child(i).child('name').get().val()
                val1 = db.child('dishes').child(i).child('description').get().val()
                val2 = str(db.child('dishes').child(i).child('price').get().val())
                val=val.lower()
                val1=val1.lower()
                val2=val2.lower()
                value=value.lower()
                # if uid we want is value then
                # we will store that in requid
                if (val == value or val1 == value or val2 == value):
                    requid = i
            print(requid)
            if requid=='null':
                return render(request, "search.html")
            print(requid)
              
            # then we will retrieve all the data related to that uid
            name = db.child('dishes').child(requid).child('name').get().val()
            description = db.child('dishes').child(requid).child('description').get().val()
            price = str(db.child('dishes').child(requid).child('price').get().val())

            Name = []
            Name.append(name)
            Description = []
            Description.append(description)
            Price = []
            Price.append(price)
            comb_lis = zip(Description, Name, Price)
              
            # send all data in zip form to searchusers.html
            return render(request, "searchdishes.html", {"comb_lis": comb_lis})