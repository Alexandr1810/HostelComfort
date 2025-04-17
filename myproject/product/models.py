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
    