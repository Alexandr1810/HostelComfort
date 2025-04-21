from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Hotel, Room, Clients, Reservations, User
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist

def hotel(request):
    hotel = Hotel.objects.all()
    return render(request, 'hotel/index.html', {'hotel': hotel})

def hotel_detail(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    context = {
        'hotel': hotel,
        'client': request.user.clients if request.user.is_authenticated else None
    }
    return render(request, 'hotel/hotel_info.html', context)

def booking(request, id):
<<<<<<< HEAD
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
=======
    hotel = get_object_or_404(Hotel, id=id)
    return render(request, 'hotel/booking.html', {'hotel': hotel})

def booking_info(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    return render(request, 'hotel/booking_info.html', {'hotel': hotel})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Clients.objects.create(
                user=user,
                phio=form.cleaned_data['phio'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                passport_seria=form.cleaned_data['passport_seria'],
                passport_num=form.cleaned_data['passport_num']
            )
            login(request, user)
            return redirect('hotel')  # Перенаправляем на главную страницу
        else:
            # Добавляем сообщения об ошибках
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
        messages.error(request, 'Неверный телефон/email или пароль')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    try:
        client = request.user.clients  # Пытаемся получить связанного клиента
    except ObjectDoesNotExist:
        # Если клиент не существует, перенаправляем на заполнение профиля
        return redirect('complete_profile')
    reservations = Reservations.objects.filter(client_id=client)
    return render(request, 'profile/user.html', {
        'client': client,
        'reservations': reservations
    })
>>>>>>> ec21fd3f5b4b67e386a4fb090478e03e638ca386
