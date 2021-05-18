from django.db import models
import json
from pyasn1_modules.rfc2459 import Name
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
data = db.child('dishes').shallow().get().val()
orderslist = []
comb_list = []
# append all the id in uidlist
flag = False
valueToDelete = '2021-04-27'

