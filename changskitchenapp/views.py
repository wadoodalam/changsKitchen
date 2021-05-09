from django.shortcuts import (get_object_or_404,  render,  HttpResponseRedirect,)
from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DishAddForm
# Create your views here.

def  Home (request):
    return render (request, "home.html")

def  Menu (request):
    return render (request, "menu.html")

def  Food (request):
    return render (request, "food.html")

def  Order (request):
    return render (request, "order.html")

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


