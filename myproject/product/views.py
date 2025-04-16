from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def kras(request):
    return render(request, 'kras/index.html')

def stolbi (request):
    return render (request, 'kras/stolbi_kras.html')

def home(request):
    items = Item.objects.all()
    return render(request, 'product/home.html', {'items': items})