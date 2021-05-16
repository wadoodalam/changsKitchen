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

valueToDelete = 'def'

data = db.child('dishes').shallow().get().val()
uidlist = []
flag = False
for i in data:
    uidlist.append(i)

for i in uidlist:
    val_del = db.child('dishes').child(i).child('name').get().val()
    val_del = val_del.lower()
    valueToDelete = valueToDelete.lower()
    if (valueToDelete == val_del):
        requ_del_id = i
        flag = True
    if flag:
        db.child('dishes').child(requ_del_id).remove()



