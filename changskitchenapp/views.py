from django.shortcuts import (get_object_or_404,  render,  HttpResponseRedirect,)
from django.views.generic import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.http import HttpResponse
import csv
import logging
from itertools import chain
# Create your views here.

def  Home (request):
    return render (request, "home.html")