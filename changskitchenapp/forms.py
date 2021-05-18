from django import forms
from django_select2 import forms as s2forms
import pyrebase
import logging

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

logger = logging.getLogger(__name__)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
data = db.child('dishes').shallow().get().val()
CURR_DISHES = []
for entry in data:
    name = db.child('dishes').child(entry).child('name').get().val()
    CURR_DISHES.append((entry, name))
logger.error(CURR_DISHES)

class DishAddForm(forms.Form):
    description= forms.CharField(max_length=1000)
    name= forms.CharField(max_length=1000)
    price= forms.FloatField()
    
    def clean(self):
        cleaned_data = super(DishAddForm, self).clean()
        description = cleaned_data.get('description')
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        if not description or not name or not price:
            raise forms.ValidationError('You have to write something!')
        data = {"description":description,"name": name,"price": price}
        db.child('dishes').push(data)

class DishEditForm(forms.Form):
    description= forms.CharField(max_length=1000)
    name= forms.CharField(max_length=1000)
    price= forms.FloatField()
    
    def clean(self):
        cleaned_data = super(DishEditForm, self).clean()
        description = cleaned_data.get('description')
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        if not description or not name or not price:
            raise forms.ValidationError('You have to write something!')
        #search the id by name
        data = db.child('dishes').shallow().get().val()
        uidlist = []
        for i in data:
            uidlist.append(i)
        for i in uidlist:
            nameToCheck = str(db.child('dishes').child(i).child('name').get().val())
            nameToCheck = nameToCheck.lower()
            if (name == nameToCheck):
                requ_edit_id = i
        db.child('dishes').child(requ_edit_id).update({"description":description,"name": name,"price": price})
class DateInput(forms.DateInput):
    input_type = 'date'

class MenuAddForm(forms.Form):

    date= forms.DateField( widget=DateInput)
    day= forms.CharField(max_length=1000)
    dishes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CURR_DISHES
    )
    
    def clean(self):
        cleaned_data = super(MenuAddForm, self).clean()
        date = str(cleaned_data.get('date'))
        day = cleaned_data.get('day')
        dishes = cleaned_data.get('dishes')
        logger.error(dishes)
        # the date can be null and the message This field is required is still displayed on the front end. Needs fixing
        if not date or not day or not dishes:
            raise forms.ValidationError('You have to write something!')
        data = {"date":date,"day": day}
        db.child('menus').child(date).set(data)
        i = 0
        for dish in dishes:
            db.child('menus').child(date).child('dishes').child(i).set(dish)
            i += 1
