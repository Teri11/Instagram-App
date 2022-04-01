from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    templates =loader.get_template('navbar.html')
    return HttpResponse(templates.render())
