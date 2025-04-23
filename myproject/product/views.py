from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
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
    # Используем hotel_id вместо hotel
    rooms = Room.objects.filter(hotel_id=hotel.id)
    
    client = None
    if request.user.is_authenticated:
        try:
            client = request.user.clients
        except User.clients.RelatedObjectDoesNotExist:
            pass
    
    context = {
        'hotel': hotel,
        'rooms': rooms,
        'client': client
    }
    return render(request, 'hotel/hotel_info.html', context)

def booking(request, id):
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

def is_manager(user):
    return user.role == 'manager'

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    hotels = Hotel.objects.all()
    clients = Clients.objects.all()
    return render(request, 'manager/dashboard.html', {
        'hotels': hotels,
        'clients': clients
    })

@login_required
@user_passes_test(is_manager)
def edit_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    if request.method == 'POST':
        # Логика обновления отеля
        hotel.name = request.POST.get('name')
        hotel.address = request.POST.get('address')
        hotel.save()
        return redirect('manager_dashboard')
    return render(request, 'manager/edit_hotel.html', {'hotel': hotel})

@login_required
@user_passes_test(is_manager)
def edit_client(request, id):
    client = get_object_or_404(Clients, id=id)
    if request.method == 'POST':
        # Логика обновления клиента
        client.phio = request.POST.get('phio')
        client.phone = request.POST.get('phone')
        client.save()
        return redirect('manager_dashboard')
