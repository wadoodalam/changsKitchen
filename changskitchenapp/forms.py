from django import forms

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

class DishAddForm(forms.Form):
    descrption= forms.CharField(max_length=1000)
    name= forms.CharField(max_length=1000)
    price= forms.FloatField()
    
    def clean(self):
        cleaned_data = super(DishAddForm, self).clean()
        descrption = cleaned_data.get('descrption')
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        if not descrption and not name and not price:
            raise forms.ValidationError('You have to write something!')
        data = {"descrption":descrption,"name": name,"price": price}
        db.child('dishes').push(data)