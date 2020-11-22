from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Форма регистрации

    """
    email = forms.EmailField(
        label='Адрес электронной почты',
        max_length=254,
        help_text='Обязатаельное поле',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    """
    Форма входа

    """
    username = forms.CharField(label='Имя пользователя или адрес электронной почты')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User


