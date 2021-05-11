from django.db import models
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
Description = [] 
Name = []
Price = []
comb_list = []
data = db.child('dishes').shallow().get().val()
dish_list = []
for i in data:
    dish_list.append(i)

for i in dish_list:
    description = db.child('dishes').child(i).child('descrption').get().val()
    Description.append(description)
    name = db.child('dishes').child(i).child('name').get().val()
    Name.append(name)
    price = str(db.child('dishes').child(i).child('price').get().val())
    Price.append(price)
    comb_list = Description+Name+Price
    


