from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    name = models.CharField('Название', max_length=50)
    address = models.CharField('Адрес', max_length=50)
    contact_phone = models.CharField('Контактный номер', max_length=11)
    email = models.CharField('Email', max_length=100)
    description = models.CharField('Описание', max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        (0, 'Одноместный'),
        (1, 'Двуместный'),
        (2, 'Люкс'),
    ]
    room_number = models.IntegerField('Номер комнаты')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    type = models.IntegerField('Тип комнаты', choices=ROOM_TYPE_CHOICES)
    minbar = models.BooleanField('Мини-Бар', default=True)
    conditioner = models.BooleanField('Кондиционер', default=True)
    television = models.BooleanField('Телевизор', default=True)
    hairdryer = models.BooleanField("Фен", default = True)
    safe = models.BooleanField("Сейф в номере", default = True)
    Kettle_or_coffee_maker = models.BooleanField("Чайник или кофеварка", default = True)
    Sound_insulation = models.BooleanField("Звукоизоляция", default = True)
    Balcony_or_terrace = models.BooleanField("Балкон или терраса", default = True)
    special_for_ivalid = models.BooleanField("Удобства для людей с ограниченными возможностями", default = True)
    Telephone = models.BooleanField("Телефон", default = True)
    Fridge = models.BooleanField("Холодильник", default = True)
    Underfloor_heating = models.BooleanField("Пол с подогревом", default = True)
    Work_facilities = models.BooleanField("Удобства для работы", default = True)
    Baby_cot_services = models.BooleanField("Услуги по предоставлению детской кроватки", default = True)
    price = models.IntegerField('Цена')

    def __str__(self):
        room_num_display = f" №{self.room_number}" if self.room_number else ""
        return f"{self.get_type_display()}{room_num_display} (Отель: {self.hotel_id.name})"
    
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    phio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Телефонный номер', max_length=11)
    email = models.CharField('Email', max_length=100)
    passport_seria = models.IntegerField('Серия паспорта')
    passport_num = models.IntegerField('Номер паспорта')

    def __str__(self):
        return self.phio
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Reservations(models.Model):
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='Клиент')
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    check_in_date = models.DateTimeField('Дата заезда')
    departure_date = models.DateTimeField('Дата выезда')
    total_amount = models.IntegerField('Общая сумма')

    def __str__(self):
        return f"Бронирование #{self.id} - {self.client_id.phio}"
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

class Reviews_and_ratings(models.Model):
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='Клиент')
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    estimation = models.IntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField('Комментарий', max_length=200)
    date = models.DateTimeField('Дата публикации', auto_now_add=True)
    
    def clean(self):
      if self.departure_date <= self.check_in_date:
        raise ValidationError("Дата выезда должна быть позже даты заезда")
    
    def __str__(self):
        return f"Отзыв от {self.client_id.phio} ({self.estimation}/5)"
    
    class Meta:
        verbose_name = 'Отзыв и оценка'
        verbose_name_plural = 'Отзывы и оценки'

