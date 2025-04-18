from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Hotel

# Create your views here.
def hotel(request):
    return render(request, 'hotel/index.html')

def hotel_info(request):
    return render(request, 'hotel/hotel_info.html')
  
def booking(request):
    return render(request, 'hotel/booking.html')

def booking_info(request):
    return render(request, 'hotel/booking_info.html')

def login(request):
    return render(request, 'registration/login.html')
  
def register(request):
    return render(request, 'registration/register.html')

def profile(request):
    return render (request, 'profile/user.html')

def hotel(request):
    hotel = Hotel.objects.all()
    return render(request, 'hotel/index.html', {'hotel': hotel})