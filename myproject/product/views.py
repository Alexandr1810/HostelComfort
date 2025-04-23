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

from django.utils import timezone
from .models import Reviews_and_ratings
from django.contrib import messages

def hotel_detail(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    rooms = Room.objects.filter(hotel_id=hotel.id)
    
    client = None
    if request.user.is_authenticated:
        try:
            client = request.user.clients
        except User.clients.RelatedObjectDoesNotExist:
            pass

    if request.method == 'POST':
        if client:
            estimation = request.POST.get('estimation', 5)
            comment = request.POST.get('comment', '').strip()
            if comment:
                Reviews_and_ratings.objects.create(
                    client_id=client,
                    hotel_id=hotel,
                    estimation=estimation,
                    comment=comment,
                    date=timezone.now()
                )
                messages.success(request, 'Ваш отзыв успешно добавлен.')
                return redirect('hotel_detail', id=hotel.id)
        else:
            messages.error(request, 'Для добавления отзыва необходимо войти в систему.')

    comments = Reviews_and_ratings.objects.filter(hotel_id=hotel).order_by('-date')

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'client': client,
        'comments': comments,
    }
    return render(request, 'hotel/hotel_info.html', context)

from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.db.models import Q

@login_required
def booking(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    client = None
    try:
        client = request.user.clients
    except User.clients.RelatedObjectDoesNotExist:
        return HttpResponseForbidden("Профиль клиента не найден. Пожалуйста, заполните профиль.")

    # Initialize filters
    room_type = request.POST.get('room_type')
    amenities = {
        'minbar': request.POST.get('minbar') == 'on',
        'conditioner': request.POST.get('conditioner') == 'on',
        'tv': request.POST.get('tv') == 'on',
        'hairdryer': request.POST.get('hairdryer') == 'on',
        'safe': request.POST.get('safe') == 'on',
        'Kettle_or_coffee_maker': request.POST.get('Kettle_or_coffee_maker') == 'on',
        'Sound_insulation': request.POST.get('Sound_insulation') == 'on',
        'Balcony_or_terrace': request.POST.get('Balcony_or_terrace') == 'on',
        'special_for_ivalid': request.POST.get('special_for_ivalid') == 'on',
        'Telephone': request.POST.get('Telephone') == 'on',
        'Fridge': request.POST.get('Fridge') == 'on',
        'Underfloor_heating': request.POST.get('Underfloor_heating') == 'on',
        'Work_facilities': request.POST.get('Work_facilities') == 'on',
        'Baby_cot_services': request.POST.get('Baby_cot_services') == 'on',
    }

    check_in_date = request.POST.get('check_in_date')
    departure_date = request.POST.get('departure_date')

    # Start with all rooms in the hotel
    rooms = Room.objects.filter(hotel_id=hotel.id)

    # Filter by room type if specified
    if room_type is not None and room_type != '':
        rooms = rooms.filter(type=int(room_type))

    # Filter by amenities
    for amenity, selected in amenities.items():
        if selected:
            filter_kwargs = {amenity: True}
            rooms = rooms.filter(**filter_kwargs)

    # Filter out rooms that are already booked for the selected dates
    if check_in_date and departure_date:
        check_in = parse_date(check_in_date)
        departure = parse_date(departure_date)
        if check_in and departure and check_in < departure:
            overlapping_reservations = Reservations.objects.filter(
                room_id__in=rooms,
                check_in_date__lt=departure,
                departure_date__gt=check_in
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=overlapping_reservations)
        else:
            messages.error(request, "Дата выезда должна быть позже даты заезда.")

    if request.method == 'POST' and 'room_number' in request.POST:
        room_numbers = request.POST.getlist('room_number')
        if not room_numbers or not check_in_date or not departure_date:
            messages.error(request, "Пожалуйста, заполните все поля.")
        else:
            check_in = parse_date(check_in_date)
            departure = parse_date(departure_date)
            if check_in >= departure:
                messages.error(request, "Дата выезда должна быть позже даты заезда.")
            else:
                successful_bookings = 0
                for room_number in room_numbers:
                    try:
                        room = Room.objects.get(room_number=room_number, hotel_id=hotel.id)
                    except Room.DoesNotExist:
                        messages.error(request, f"Комната с номером {room_number} не найдена.")
                        continue

                    # Check if room is available for the dates
                    overlapping_reservations = Reservations.objects.filter(
                        room_number=room_number,
                        check_in_date__lt=departure,
                        departure_date__gt=check_in
                    )
                    if overlapping_reservations.exists():
                        messages.error(request, f"Комната с номером {room_number} уже забронирована на выбранные даты.")
                        continue

                    nights = (departure - check_in).days
                    total_amount = hotel.price * nights
                    Reservations.objects.create(
                        client_id=client,
                        room_number=room_number,
                        check_in_date=check_in,
                        departure_date=departure,
                        total_amount=total_amount
                    )
                    successful_bookings += 1

                if successful_bookings > 0:
                    messages.success(request, f"Успешно забронировано {successful_bookings} комнат(ы).")
                    return redirect('user_profile')

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'selected_room_type': room_type,
        'selected_amenities': amenities,
        'check_in_date': check_in_date,
        'departure_date': departure_date,
    }
    return render(request, 'hotel/booking.html', context)

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
    if request.user.is_superuser:
        # Для суперпользователя можно вернуть пустой профиль или специальную страницу
        client = None
        reservations = []
    else:
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
