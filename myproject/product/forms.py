from django import forms
from .models import Hotel, Room
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Телефон или Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150, required=True)
    phio = forms.CharField(label='ФИО', max_length=100, required=True)
    phone = forms.CharField(label='Телефон', max_length=11, required=True)
    email = forms.EmailField(label='Email', required=True)
    passport_seria = forms.IntegerField(label='Серия паспорта', required=True)
    passport_num = forms.IntegerField(label='Номер паспорта', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                 'phio', 'phone', 'passport_seria', 'passport_num')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Add(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'contact_phone', 'email', 'description', 'rating']
        labels = {
            "name": "Имя",
            "address": "Адрес",
            "contact_phone": "Контактный номер",
            "email": "Email",
            "description": "Описание",
            "rating": "Рейтинг",
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number', 'type', 'minbar', 'conditioner', 'television', 'hairdryer', 'safe',
            'Kettle_or_coffee_maker', 'Sound_insulation', 'Balcony_or_terrace', 'special_for_ivalid',
            'Telephone', 'Fridge', 'Underfloor_heating', 'Work_facilities', 'Baby_cot_services', 'price'
        ]
        labels = {
            'room_number': 'Номер комнаты',
            'type': 'Тип комнаты',
            'minbar': 'Мини-Бар',
            'conditioner': 'Кондиционер',
            'television': 'Телевизор',
            'hairdryer': 'Фен',
            'safe': 'Сейф в номере',
            'Kettle_or_coffee_maker': 'Чайник или кофеварка',
            'Sound_insulation': 'Звукоизоляция',
            'Balcony_or_terrace': 'Балкон или терраса',
            'special_for_ivalid': 'Удобства для людей с ограниченными возможностями',
            'Telephone': 'Телефон',
            'Fridge': 'Холодильник',
            'Underfloor_heating': 'Пол с подогревом',
            'Work_facilities': 'Удобства для работы',
            'Baby_cot_services': 'Услуги по предоставлению детской кроватки',
            'price': 'Цена',
        }
