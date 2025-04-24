from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Телефон или Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    phio = forms.CharField(label='ФИО', max_length=100, required=True)
    phone = forms.CharField(label='Телефон', max_length=11, required=True)
    email = forms.EmailField(label='Email', required=True)
    passport_seria = forms.IntegerField(label='Серия паспорта', required=True)
    passport_num = forms.IntegerField(label='Номер паспорта', required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2',
                 'phio', 'phone', 'passport_seria', 'passport_num')
        
