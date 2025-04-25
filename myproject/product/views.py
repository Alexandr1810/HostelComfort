from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Hotel, Room, Clients, Reservations, User, Reviews_and_ratings
from django.contrib import messages
from .forms import RegisterForm, LoginForm, Add
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test

@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Reviews_and_ratings, id=id)
    user = request.user
    if user.is_superuser or (hasattr(user, 'clients') and comment.client_id == user.clients):
        if request.method == "POST":
            hotel_id = comment.hotel_id.id
            comment.delete()
            messages.success(request, "Комментарий успешно удалён.")
            return redirect('hotel_detail', id=hotel_id)
        else:
            return HttpResponseForbidden("Неверный метод запроса.")
    else:
        return HttpResponseForbidden("У вас нет прав на удаление этого комментария.")

def hotel(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Amenities filter from GET parameters
    amenities_filters = {
        'minbar': request.GET.get('minbar') == 'on',
        'conditioner': request.GET.get('conditioner') == 'on',
        'tv': request.GET.get('tv') == 'on',
        'hairdryer': request.GET.get('hairdryer') == 'on',
        'safe': request.GET.get('safe') == 'on',
        'Kettle_or_coffee_maker': request.GET.get('Kettle_or_coffee_maker') == 'on',
        'Sound_insulation': request.GET.get('Sound_insulation') == 'on',
        'Balcony_or_terrace': request.GET.get('Balcony_or_terrace') == 'on',
        'special_for_ivalid': request.GET.get('special_for_ivalid') == 'on',
        'Telephone': request.GET.get('Telephone') == 'on',
        'Fridge': request.GET.get('Fridge') == 'on',
        'Underfloor_heating': request.GET.get('Underfloor_heating') == 'on',
        'Work_facilities': request.GET.get('Work_facilities') == 'on',
        'Baby_cot_services': request.GET.get('Baby_cot_services') == 'on',
    }

    hotels = Hotel.objects.all()

    if min_price:
        try:
            min_price_val = float(min_price)
            hotels = hotels.filter(price__gte=min_price_val)
        except ValueError:
            pass
    if max_price:
        try:
            max_price_val = float(max_price)
            hotels = hotels.filter(price__lte=max_price_val)
        except ValueError:
            pass

    # Filter rooms by amenities
    rooms = Room.objects.all()
    for amenity, selected in amenities_filters.items():
        if selected:
            filter_kwargs = {amenity: True}
            rooms = rooms.filter(**filter_kwargs)

    # Get hotel ids from filtered rooms
    hotel_ids = rooms.values_list('hotel_id', flat=True).distinct()

    # Filter hotels by hotel_ids
    hotels = hotels.filter(id__in=hotel_ids)

    # Fetch rooms for each hotel and add room_types attribute
    for hotel in hotels:
        rooms = Room.objects.filter(hotel_id=hotel.id)
        room_types = set(room.get_type_display() for room in rooms)
        hotel.room_types = room_types

    context = {
        'hotel': hotels,
        'min_price': min_price,
        'max_price': max_price,
        'selected_amenities': amenities_filters,
    }
    return render(request, 'hotel/index.html', context)

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


@login_required
def booking(request, id, room_number=None):
    hotel = get_object_or_404(Hotel, id=id)
    client = None
    try:
        client = request.user.clients
    except User.clients.RelatedObjectDoesNotExist:
        return HttpResponseForbidden("Профиль клиента не найден. Пожалуйста, заполните профиль.")

    room = None
    if room_number:
        try:
            room = Room.objects.get(room_number=room_number, hotel_id=hotel.id)
        except Room.DoesNotExist:
            messages.error(request, f"Комната с номером {room_number} не найдена.")
            return redirect('hotel_detail', id=hotel.id)

    check_in_date = request.POST.get('check_in_date') or request.GET.get('check_in_date')
    departure_date = request.POST.get('departure_date') or request.GET.get('departure_date')

    if request.method == 'POST':
        if not check_in_date or not departure_date or not room:
            messages.error(request, "Пожалуйста, заполните все поля.")
        else:
            check_in = parse_date(check_in_date)
            departure = parse_date(departure_date)
            if not check_in or not departure or check_in >= departure:
                messages.error(request, "Дата выезда должна быть позже даты заезда.")
            else:
                overlapping_reservations = Reservations.objects.filter(
                    room_number=room.room_number,
                    check_in_date__lt=departure,
                    departure_date__gt=check_in
                )
                if overlapping_reservations.exists():
                    messages.error(request, f"Комната с номером {room.room_number} уже забронирована на выбранные даты.")
                else:
                    nights = (departure - check_in).days
                    total_amount = room.price * nights
                    Reservations.objects.create(
                        client_id=client,
                        room_number=room.room_number,
                        check_in_date=check_in,
                        departure_date=departure,
                        total_amount=total_amount
                    )
                    messages.success(request, f"Комната №{room.room_number} успешно забронирована.")
                    return redirect('user_profile')

    context = {
        'hotel': hotel,
        'room': room,
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

@login_required
def user_profile(request):
    if request.user.is_superuser:
        try:
            client = request.user.clients
        except ObjectDoesNotExist:
            # Для суперпользователя без связанного клиента создаем фиктивный клиент
            class DummyClient:
                def __init__(self, user):
                    self.phio = user.get_full_name() or user.username
                    self.phone = "N/A"
                    self.email = user.email or "N/A"
                    self.passport_seria = "N/A"
                    self.passport_num = "N/A"
            client = DummyClient(request.user)
        reservations = Reservations.objects.all()
        return render(request, 'profile/manager.html', {
            'client': client,
            'reservations': reservations
        })
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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('hotel_manager')
                else:
                    return redirect('user_profile')
        messages.error(request, 'Неверный телефон/email или пароль')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add(request):
    if request.method == "POST":
        form = Add(request.POST)
        if form.is_valid():
            Hotel = form.save(commit=False)
            Hotel.owner = request.user
            Hotel.save()
            return redirect('hotel')
    else:
        form = Add()
    return render(request, 'product/add.html', {'form': form})

@login_required
def delete(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    if request.method == "POST":
        hotel.delete()
        return redirect('hotel')
    return render(request, 'product/delete.html', {'hotel': hotel})

@login_required
def edit(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    if request.method == "POST":
        form = Add(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel')
    else:
        form = Add(instance=hotel)
    return render(request, 'product/edit.html', {'form': form})

@login_required
def cancel_booking(request, booking_id):
    try:
        reservation = Reservations.objects.get(id=booking_id, client_id=request.user.clients)
    except Reservations.DoesNotExist:
        messages.error(request, "Бронирование не найдено или у вас нет прав на его удаление.")
        return redirect('user_profile')

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Бронирование успешно снято.")
        return redirect('user_profile')

    return render(request, 'profile/cancel.html', {'reservation': reservation})
