from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Hotel(models.Model):
    name = models.CharField('Название', max_length=50)
    address = models.CharField('Адрес', max_length=50)
    contact_phone = models.CharField('Контактный номер', max_length=11)
    email = models.CharField('Email', max_length=100)
    description = models.CharField('Описание', max_length=100)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    price = models.IntegerField('Цена', max_length=50)

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

    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.IntegerField('Тип комнат', choices=ROOM_TYPE_CHOICES)
    minbar = models.BooleanField('Мини-Бар', default=True)
    conditioner = models.BooleanField('Кондиционер', default=True)

    def __str__(self):
        return self.hotel_id
    
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Clients(models.Model):
    phio  = models.CharField('ФИО', max_length=100)
    phone  = models.CharField('Телефонный номер', max_length=11)
    email = models.CharField('Email', max_length=100)
    password = models.CharField('Пароль', max_length=200)
    passport_seria = models.IntegerField('Серия паспорта', max_length=100)
    passport_num = models.IntegerField('Номер паспорта', max_length=100)

    def __str__(self):
        return self.phio
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Reservations(models.Model):
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField('Дата заезда')
    departure_date = models.DateTimeField('Дата выезда')
    total_amount = models.IntegerField('Общая сумма')
    

    def __str__(self):
        return self.client_id
    
    class Meta:
        verbose_name_plural = 'Отношения'

class Reviews_and_ratings(models.Model):
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    estimation  = models.IntegerField('Оценка')
    comment = models.CharField('Комментарий', max_length=200)
    date  = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.client_id
    
    class Meta:
        verbose_name_plural = 'Отзывы и оценки'