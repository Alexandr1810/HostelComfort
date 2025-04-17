from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Hotel(models.Model):
    name = models.CharField('Название', max_length=50)
    address = models.CharField('Адрес', max_length=50)
    contact_phone = models.CharField('Контактный номер', max_length=11)
    email = models.CharField('Email')
    description = models.CharField('Описание', max_length=100)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

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
    surname_user = models.CharField('Фамилия', max_length=50)
    name_user = models.CharField('Имя', max_length=50)
    patronymic_user = models.CharField('Отчество', max_length=50)
    email = models.CharField('Email')
    passport_number = models.CharField('Паспортные данные', max_length=20, unique=True)
    address = models.CharField('Адрес', max_length=50)
    
    def __str__(self):
        return self.surname_user
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Reservations(models.Model):

    STATUS_CHOICES = [
        ('available', 'Доступно'),
        ('occupied', 'Занято'),
    ]

    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    surname_user = models.CharField('Фамилия', max_length=50)
    check_in_date = models.DateField('Дата заезда')
    departure_date = models.DateField('Дата выезда')
    total_amount = models.IntegerField('Общее количество')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
   
    
    def __str__(self):
        return self.surname_user
    
    class Meta:
        verbose_name_plural = 'Отношения'


class Reviews_and_ratings(models.Model):
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    surname_user = models.CharField('Фамилия', max_length=50)
    estimation = models.IntegerField('Оценка')
    comment = models.CharField('Комментарий', max_length=300)
    date = models.DateField('Дата')
   
    
    def __str__(self):
        return self.surname_user
    
    class Meta:
        verbose_name_plural = 'Отзывы и оценки'

