from django.db import models
from .forms import DishAddForm
from .views import Food_Add
import json
# Create your models here.

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

#class FoodAdd():
 #   description = Food_Add.descrption
    

# name = DishAddForm.clean.name
   # price = DishAddForm.price.clean.price
   # data = {"description":description,"name": name,"price": price}
    #db.push(data)
#data={"name":"John", "age" : "12"}
#db.push(data)

