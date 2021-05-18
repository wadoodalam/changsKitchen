from django import forms
from django_select2 import forms as s2forms
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
# fetch all the dish names
for i in data:
    orderslist.append(i)
for i in orderslist:

    name = db.child('dishes').child(i).child('name').get().val()
    
    food = {
        "name": name,
    }
    comb_list.append(food)

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
    def ConvertToString(items):
        result = ""
        for i in items:
            result += str(str(i["name"]) + "; ")
        return result[0:-2]
    
    Dish_Choices = ConvertToString(comb_list)
    date= forms.DateField( widget=DateInput)

    # the field that displays all the dish choices
    dishes = forms.ChoiceField(label='Dish', choices=Dish_Choices)
    
    def clean(self):
        cleaned_data = super(MenuAddForm, self).clean()
        date = str(cleaned_data.get('date'))

        dishNamesFromDBCoresspondingFromUser = []
       
        #list of dishes seleted from the user returned
        dishNamesFromUser = []
        dishNamesFromUser = cleaned_data.get('dishes')

        # this code fetches the dishes from db corresponding to name of the dish selected by the user
        for dishid in dishNamesFromUser:
            name = db.child('dishes').child(i).child('name').get().val()
            description = db.child('dishes').child(i).child('description').get().val()
            price = str(db.child('dishes').child(i).child('price').get().val())
            food = {
                "name": name,
                "description": description,
                "price": price
            }
            dishNamesFromDBCoresspondingFromUser.append(data)

        # the date can be null and the message This field is required is still displayed on the front end. Needs fixing
        if not date or not dishNamesFromUser:
            raise forms.ValidationError('You have to write something!')
        data = {"date":date, "dishNamesFromDBCoresspondingFromUser":dishNamesFromDBCoresspondingFromUser}
        db.child('menus').child(date).set(data)
        i = 0
        for dish in dishNamesFromUser:
            db.child('menus').child(date).child('dishes').child(i).set(dish)
            i += 1
