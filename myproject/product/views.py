from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Hotel, Room

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

def hotel_info(request):
    hotel_info = Room.objects.all()
    return render(request, 'hotel/hotel_info.html', {'hotel_info': hotel_info})

def hotel_info(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'hotel/hotel_info.html', {'hotel': hotel})

def booking(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'booking.html', {'hotel': hotel})

def booking_info(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'booking_info.html', {'hotel': hotel})


def hotel_1(request):
    return render(request, 'frontend/hotel/index.html')

def hotel_info_1(request):
    return render(request, 'frontend/hotel/hotel_info.html')
  
def booking_1(request):
    return render(request, 'frontend/hotel/booking.html')

def booking_info_1(request):
    return render(request, 'frontend/hotel/booking_info.html')

def login_1(request):
    return render(request, 'frontend/registration/login.html')
  
def register_1(request):
    return render(request, 'frontend/registration/register.html')

def profile_1(request):
    return render (request, 'frontend/profile/user.html')

def hotel_1(request):
    hotel = Hotel.objects.all()
    return render(request, 'frontend/hotel/index.html', {'hotel': hotel})

def hotel_info_1(request):
    hotel_info_1 = Room.objects.all()
    return render(request, 'frontend/hotel/hotel_info.html', {'hotel_info_1': hotel_info_1})
