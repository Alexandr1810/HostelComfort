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
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    hotels = Hotel.objects.all()
    if min_price:
        try:
            min_price_val = int(min_price)
            hotels = hotels.filter(price__gte=min_price_val)
        except ValueError:
            pass
    if max_price:
        try:
            max_price_val = int(max_price)
            hotels = hotels.filter(price__lte=max_price_val)
        except ValueError:
            pass
    return render(request, 'hotel/index.html', {'hotel': hotels})

def hotel_info(request):
    hotel_info = Room.objects.all()
    return render(request, 'hotel/hotel_info.html', {'hotel_info': hotel_info})

def hotel_info(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'hotel/hotel_info.html', {'hotel': hotel})

def booking(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'hotel/booking.html', {'hotel': hotel})

def booking_info(request, id):
    hotel = get_object_or_404(Hotel, id=id)  # Получаем отель по ID
    return render(request, 'hotel/booking_info.html', {'hotel': hotel})

