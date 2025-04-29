from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Hotel, Room, Clients, Reservations, User, Reviews_and_ratings
from .forms import RegisterForm, LoginForm, Add, RoomForm

# папка Hotel
def hotel(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    # Фильтр удобств по полученным параметрам
    amenities_filters = {
        'minbar': request.GET.get('minbar') == 'on',
        'conditioner': request.GET.get('conditioner') == 'on',
        'television': request.GET.get('television') == 'on',
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
    # Проверяет применены ли какие-либо фильтры
    filters_applied = any([
        min_price,
        max_price,
        any(amenities_filters.values())
    ])
    if filters_applied:
        # Фильтер номера по удобствам и цене
        rooms = Room.objects.all()
        if min_price:
            try:
                min_price_val = float(min_price)
                rooms = rooms.filter(price__gte=min_price_val)
            except ValueError:
                pass
        if max_price:
            try:
                max_price_val = float(max_price)
                rooms = rooms.filter(price__lte=max_price_val)
            except ValueError:
                pass
        for amenity, selected in amenities_filters.items():
            if selected:
                filter_kwargs = {amenity: True}
                rooms = rooms.filter(**filter_kwargs)
        # Получение идентификаторов отелей из отфильтрованных номеров
        hotel_ids = rooms.values_list('hotel_id', flat=True).distinct()
        # Отфильтрованные отели по идентификаторам hotel_id
        hotels = Hotel.objects.filter(id__in=hotel_ids)
    else:
        # Фильтры не применяются, отображаются все отели
        hotels = Hotel.objects.all()
    # Выберает номера для каждого отеля и добавляет атрибут room_types и минимальную цену
    for hotel in hotels:
        rooms = Room.objects.filter(hotel_id=hotel.id)
        room_types = set(room.get_type_display() for room in rooms)
        hotel.room_types = room_types
        min_price_room = rooms.order_by('price').first()
        hotel.price = min_price_room.price if min_price_room else None
    context = {
        'hotel': hotels,
        'min_price': min_price,
        'max_price': max_price,
        'selected_amenities': amenities_filters,
    }
    return render(request, 'hotel/index.html', context)

def hotel_info(request, id):
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
                return redirect('hotel_info', id=hotel.id)
        else:
            messages.error(request, 'Для добавления отзыва необходимо войти в систему.')
    comments = Reviews_and_ratings.objects.filter(hotel_id=hotel).order_by('-date')

    # Собираем множество удобств, которые есть хотя бы в одном номере
    amenities_set = set()
    for room in rooms:
        if room.minbar:
            amenities_set.add('Мини-Бар')
        if room.conditioner:
            amenities_set.add('Кондиционер')
        if room.television:
            amenities_set.add('Телевизор')
        if room.hairdryer:
            amenities_set.add('Фен')
        if room.safe:
            amenities_set.add('Сейф в номере')
        if room.Kettle_or_coffee_maker:
            amenities_set.add('Чайник или кофеварка')
        if room.Sound_insulation:
            amenities_set.add('Звукоизоляция')
        if room.Balcony_or_terrace:
            amenities_set.add('Балкон или терраса')
        if room.special_for_ivalid:
            amenities_set.add('Удобства для людей с ограниченными возможностями')
        if room.Telephone:
            amenities_set.add('Телефон')
        if room.Fridge:
            amenities_set.add('Холодильник')
        if room.Underfloor_heating:
            amenities_set.add('Пол с подогревом')
        if room.Work_facilities:
            amenities_set.add('Удобства для работы')
        if room.Baby_cot_services:
            amenities_set.add('Услуги по предоставлению детской кроватки')

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'client': client,
        'comments': comments,
        'amenities_set': amenities_set,
    }
    return render(request, 'hotel/hotel_info.html', context)


@login_required
def booking(request, id, room_number=None):
    hotel = get_object_or_404(Hotel, id=id)
    client = request.user.clients
    room = get_object_or_404(Room, room_number=room_number, hotel_id=hotel.id)
    
    date_error = False
    booking_conflict = False

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        departure_date = request.POST.get('departure_date')
        
        if check_in_date and departure_date:
            try:
                check_in = timezone.datetime.strptime(check_in_date, '%Y-%m-%d').date()
                departure = timezone.datetime.strptime(departure_date, '%Y-%m-%d').date()
                
                if departure <= check_in:
                    date_error = True
                else:
                    # Проверка доступности номера
                    if not Reservations.objects.filter(
                        room_id=room,
                        check_in_date__lt=departure,
                        departure_date__gt=check_in
                    ).exists():
                        # Создаем бронирование без оплаты
                        Reservations.objects.create(
                            client_id=client,
                            room_id=room,
                            check_in_date=check_in,
                            departure_date=departure,
                            total_amount=room.price * (departure - check_in).days,
                        )
                        return redirect('booking_info', id=hotel.id)
                    else:
                        booking_conflict = True
            except ValueError:
                messages.error(request, "Неверный формат даты.")

    context = {
        'hotel': hotel,
        'room': room,
        'date_error': date_error,
        'booking_conflict': booking_conflict,
    }
    return render(request, 'hotel/booking.html', context)

@login_required
def booking_info(request, id, room_number=None):
    hotel = get_object_or_404(Hotel, id=id)
    room = None
    reservation = None
    
    if room_number:
        room = get_object_or_404(Room, hotel_id=hotel.id, room_number=room_number)
        if request.user.is_authenticated:
            try:
                client = request.user.clients
                reservation = Reservations.objects.filter(
                    client_id=client, 
                    room_id=room
                ).latest('check_in_date')
            except (Reservations.DoesNotExist, AttributeError):
                pass
    
    context = {
        'hotel': hotel,
        'room': room,
        'reservation': reservation,
    }
    return render(request, 'hotel/booking_info.html', context)
  
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            Clients.objects.create(
                user=user,
                phio=form.cleaned_data['phio'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                passport_seria=form.cleaned_data['passport_seria'],
                passport_num=form.cleaned_data['passport_num']
            )
            login(request, user)
            return redirect('hotel')
        else:
            messages.error(request, "Ошибка регистрации: " + str(form.errors))
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
                if user.is_superuser:
                    return redirect('hotel_manager')
                else:
                    return redirect('user_profile')
        messages.error(request, 'Неверный телефон/email или пароль')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
  
# Выход из аккаунта 
def user_logout(request):
    logout(request)
    return redirect('login')

# папка Profile
@login_required
def user_profile(request):
    try:
        client = request.user.clients
    except ObjectDoesNotExist:
        # Если клиент не существует, перенаправляем на заполнение профиля
        return redirect('register')
    reservations = Reservations.objects.filter(client_id=client)
    return render(request, 'profile/user.html', {
        'client': client,
        'reservations': reservations
    })

# папка Product
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
    return render(request, 'product/cancel.html', {'reservation': reservation})

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
def comment_delete(request, id):
    comment = get_object_or_404(Reviews_and_ratings, id=id)
    user = request.user
    if user.is_superuser or (hasattr(user, 'clients') and comment.client_id == user.clients):
        if request.method == "POST":
            hotel_id = comment.hotel_id.id
            comment.delete()
            messages.success(request, "Комментарий успешно удалён.")
            return redirect('hotel_info', id=hotel_id)
        else:
            return HttpResponseForbidden("Неверный метод запроса.")
    else:
        return HttpResponseForbidden("У вас нет прав на удаление этого комментария.")

@login_required
def edit_room(request, hotel_id, room_number):
    # Проверяет, есть ли у пользователя разрешение на редактирование информации о номере
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав на редактирование информации о комнате.")
    room = get_object_or_404(Room, hotel_id=hotel_id, room_number=room_number)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f"Информация о комнате №{room_number} успешно обновлена.")
            return redirect('hotel_info', id=hotel_id)
    else:
        form = RoomForm(instance=room)
    context = {
        'form': form,
        'hotel_id': hotel_id,
        'room_number': room_number,
    }
    return render(request, 'product/edit_room.html', context)
