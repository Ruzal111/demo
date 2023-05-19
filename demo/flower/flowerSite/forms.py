from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegistrationForm(UserCreationForm):
    rules = forms.CharField(label='Я согласен с правилами регистрации', widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'last_name', 'first_name', 'patronymic')

class CreateOrderForm(forms.ModelForm):
    password = forms.CharField(label='Подтвердите паролем', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', )