from django.shortcuts import (get_object_or_404,  render,  HttpResponseRedirect,)
from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, request
from pyasn1.type.univ import Null
from .forms import DishAddForm, MenuAddForm, DishEditForm
import pyrebase
import json

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
    for i in orderslist:

        email = db.child('users').child(i).child('email').get().val()
        name = db.child('users').child(i).child('name').get().val()
        password = db.child('users').child(i).child('password').get().val()
        phone = str(db.child('users').child(i).child('phone').get().val())
        uid = db.child('users').child(i).child('uid').get().val()

        user = {
            "email": email,
            "name": name,
            "password": password,
            "phone": phone,
            "uid": uid
        }

        # the list contains the description, name and price of all dishes.
        
        comb_list.append(user)
    
    context={
        "comb_list": comb_list,
    }
    return render (request, "users.html",context)

def  Menu (request):
    data = db.child('menus').shallow().get().val()
    orderslist = []
    comb_list = []
    # append all the id in uidlist
    for i in data:
        orderslist.append(i)
    for i in orderslist:

        date = str(db.child('menus').child(i).child('date').get().val())
        day = db.child('menus').child(i).child('day').get().val()
        dishes = str(db.child('menus').child(i).child('dishes').get().val())
        
        food = {
            "date": date,
            "day": day,
            "dishes": dishes
        }
        comb_list.append(food)
        context={
        "comb_list": comb_list,
        }
    return render (request, "menu.html", context)

def  Menu_Manage (request):
    return render (request, "menu_manage.html")

def  Menu_Add (request):
    if request.method == 'POST':
        form = MenuAddForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/menu')
    else:
        form = MenuAddForm()
    return render (request, "menu_add.html",{'form': form})


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
        price = "{:10.2f}".format(db.child('dishes').child(i).child('price').get().val())
        
        food = {
            "description": description,
            "name": name,
            "price": price
        }
        comb_list.append(food)
        context={
        "comb_list": comb_list,
    }
    return render (request, "food.html", context)


def Food_Delete(request):
    valueToDelete = request.POST.get('delete')
    if valueToDelete is None or valueToDelete =="":
        return render(request, "food_delete.html")

    data = db.child('dishes').shallow().get().val()
    uidlist = []
    flag = False
    for i in data:
        uidlist.append(i)
    for i in uidlist:
        val_del = str(db.child('dishes').child(i).child('name').get().val())
        val_del = val_del.lower()
        valueToDelete = valueToDelete.lower()
        if (valueToDelete == val_del):
            requ_del_id = i
            flag = True
        if flag:
            # query to delete that child
            db.child('dishes').child(requ_del_id).remove()
            return redirect('/food')
    return render (request, "food_delete.html")

def Food_Edit(request):
    valueToEdit = request.POST.get('edit')
    if valueToEdit is None or valueToEdit =="":
        return render(request, "food_edit.html")

    data = db.child('dishes').shallow().get().val()
    uidlist = []
    comb_list = []
    flag = False
    for i in data:
        uidlist.append(i)
    for i in uidlist:
        nameToCheck = str(db.child('dishes').child(i).child('name').get().val())
        nameToCheck = nameToCheck.lower()
        valueToEdit = valueToEdit.lower()
        if (valueToEdit == nameToCheck):
            requ_edit_id = i
            #flag = True

            name = str(db.child('dishes').child(requ_edit_id).child('name').get().val())
            description = db.child('dishes').child(requ_edit_id).child('description').get().val()
            price = str(db.child('dishes').child(requ_edit_id).child('price').get().val())

            dishes  = {
                "description": description,
                "name": name,
                "price": price
            }
            comb_list.append(dishes)
    return render(request, 'food_edit.html', {"comb_list":comb_list})

                    
    

def  Order (request):
    data = db.child('orders').shallow().get().val()
    orderslist = []
    comb_list = []
    val_delete = 'null'
    # append all the id in uidlist
    for i in data:
        orderslist.append(i)
    for i in orderslist:

        date = db.child('orders').child(i).child('date').get().val()
        items = ConvertToString(db.child('orders').child(i).child('items').get().val())
        status = db.child('orders').child(i).child('status').get().val()
        stringDate = db.child('orders').child(i).child('stringDate').get().val()
        cost = str(db.child('orders').child(i).child('summaryPrice').get().val())
        tax = "{:10.2f}".format(db.child('orders').child(i).child('tax').get().val())
        tip = "{:10.2f}".format(db.child('orders').child(i).child('tip').get().val())
        finalPrice = "{:10.2f}".format(db.child('orders').child(i).child('finalPrice').get().val())
        uid = db.child('orders').child(i).child('uid').get().val()

        order = {
            "date": date,
            "finalPrice": finalPrice,
            "items": items,
            "status": status,
            "stringDate": stringDate,
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
    
def ConvertToString(items):
    result = ""
    for i in items:
        result += str(str(i["quantity"]) + " " + i["name"] + "; ")
    return result[0:-2]

def Food_Add(request):
    if request.method == 'POST':
        form = DishAddForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/food')
    else:
        form = DishAddForm()
    return render(request, 'food_add.html', {'form': form})

def Search (request):
    return render (request, "search.html")

def Menu_Delete(request):
    flag = False
    valueToDelete = request.POST.get('date')
    if valueToDelete is None or valueToDelete =="":
        return render(request, "menu_delete.html")

    dates = db.child('menus').shallow().get().val()

    if (valueToDelete in dates):
        db.child('menus').child(valueToDelete).remove()
        return redirect('/menu')
    return render (request, "menu_delete.html")

def Searchresults(request):
    value = request.POST.get('search')
    if value =="":
        return render(request, "search.html")

    title = request.POST['category']
    if title =="":
        return render(request, "search.html")
    if value is None or title is None:
        return render(request, "search.html")
    else:
        if title == "Users":
            comb_list = []
            data = db.child('users').shallow().get().val()
            uidlist = []
            requid = []
            
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
                #val2=val2.lower()
                value=value.lower()
                # if uid we want is value then
                # we will store that in requid
                if (val == value or val1 == value or val2 == value ) :
                    requid.append(i)
            if requid=='null':
                return render(request, "search.html")
            
            # then we will retrieve all the data related to that uid
            for requid in requid:
                email = db.child('users').child(requid).child('email').get().val()
                name = db.child('users').child(requid).child('name').get().val()
                phone = str(db.child('users').child(requid).child('phone').get().val())
                uid = db.child('users').child(requid).child('uid').get().val()

                user = {
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "uid": uid
                }
                comb_list.append(user)
            
            # send all data in zip form to searchusers.html
            return render(request, "searchusers.html", {"comb_list": comb_list})
        elif title == "Dishes":

            comb_list = []
            data = db.child('dishes').shallow().get().val()
            uidlist = []
            requid = []
            for i in data:
                uidlist.append(i)

            for i in uidlist:
                val = db.child('dishes').child(i).child('description').get().val()
                val1 = str(db.child('dishes').child(i).child('name').get().val())
                val2 = str(db.child('dishes').child(i).child('price').get().val())
                val=val.lower()
                val1=val1.lower()
                val2=val2.lower()
                value=value.lower()
                if (val == value or val1 == value or val2 == value):
                    requid.append(i)
            print(requid)
            if requid=='null':
                return render(request, "search.html")
            
            for requid in requid:
                name = db.child('dishes').child(requid).child('name').get().val()
                description = db.child('dishes').child(requid).child('description').get().val()
                price = str(db.child('dishes').child(requid).child('price').get().val())

                dishes  = {
                    "description": description,
                    "name": name,
                    "price": price
                }
                comb_list.append(dishes)

            return render(request, "searchdishes.html", {"comb_list": comb_list})
        elif title == "Orders":
            comb_list = []
            data = db.child('orders').shallow().get().val()
            uidlist = []
            requid = []
              
            # append all the id in uidlist
            for i in data:
                uidlist.append(i)
                  
            # if we have find all the uid then
            # we will look for the one we need    
            for i in uidlist:
                val = db.child('orders').child(i).child('date').get().val()
                val1 = str(db.child('orders').child(i).child('finalPrice').get().val())
                val2 = db.child('orders').child(i).child('items').get().val()
                val3 = db.child('orders').child(i).child('status').get().val()
                val4 = db.child('orders').child(i).child('stringDate').get().val()
                val5 = db.child('orders').child(i).child('summary').get().val()
                val6 = str(db.child('orders').child(i).child('cost').get().val())
                val7 = str(db.child('orders').child(i).child('tax').get().val())
                val8 = str(db.child('orders').child(i).child('tip').get().val())
                val9 = db.child('orders').child(i).child('uid').get().val()
                
                val=val.lower()
                val1=val1.lower()
                #val2=val2.lower()
                val3=val3.lower()
                val4=val4.lower()
                val5=val5.lower()
                val6=val6.lower()
                val7=val7.lower()
                val8=val8.lower()
                val9=val9.lower()

                value=value.lower()
                # if uid we want is value then
                # we will store that in requid
            if (val == value or val1 == value or val2 == value or val3 == value or val4 == value or val5 == value or val6 == value or val7 == value or val8 == value or val9 == value):
                requid.append(i)
            print(requid)
            if requid=='null':
                return render(request, "search.html")
            print(requid)
              
            # then we will retrieve all the data related to that uid
            for i in requid:
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
              
            # send all data in zip form to searchusers.html
            return render(request, "searchorders.html", {"comb_list": comb_list})