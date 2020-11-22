import os
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from account.forms import SignUpForm, LoginForm
from blog.settings.base import BASE_DIR
from blog.settings.base import AUTHENTICATION_BACKENDS

"""
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = os.path.join(BASE_DIR, "templates/registration/signup.html")
"""


def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким адресом уже существует')
            else:
                user = form.save()
                user.is_active = False
                current_site = get_current_site(request)
                mail_subject = 'Подтвердите регистрацию на' + current_site.domain
                template = os.path.join(BASE_DIR, 'templates/registration/account_activate.html')
                message = render_to_string(template, {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                user.save()
                messages.success(request, 'Вы успешно зарегестрировались. Вам осталось только подтвердить почту')
                return redirect('/')
    else:
        form = SignUpForm
    template = os.path.join(BASE_DIR, 'templates/registration/signup.html')
    context = {'form': form}
    return render(request, template, context)


def account_activate(request, uidb64, token):
    """Подтверждение аккаунта (Активация)"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user, backend=AUTHENTICATION_BACKENDS[0])
        messages.success(request, f'Вы подтвердили почту. Добро пожаловать, {user.username}!')
        return redirect('/')
    else:
        messages.error(request, 'Ошибка подтверждения')
        return redirect('/')


def login(request):
    """Вход в учетную запись"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, f'Добро пожаловать, {user.username}!')
                    if user.is_superuser:
                        # если суперюзер, то перенаправить сразу в админку
                        return redirect('/admin')
                    return redirect('/')
                else:
                    messages.error(request, 'Ваша учетная запись неактивна. Возможно, Вы не подтвердили её.')
                    return redirect('login')
            else:
                messages.error(request, 'Неверный логин или пароль')
                return redirect('login')
    else:
        form = LoginForm
    template = os.path.join(BASE_DIR, "templates/registration/login.html")
    context = {'form': form}
    return render(request, template, context)


def password_reset(request):
    """Восстановление пароля"""
    usermodel = get_user_model()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = usermodel.objects.get(email=email)
            except usermodel.DoesNotExist:
                messages.error(request, 'Пользователся с таким e-mail не существует')
                return redirect('password_reset')
            else:
                form.save(request=request)
                messages.success(request, 'На Вашу почту отправлено письмо с дальнейшими инструкциями')
                return redirect('/')
    else:
        form = PasswordResetForm
    template = os.path.join(BASE_DIR, "templates/registration/password_reset_form.html")
    context = {'form': form}
    return render(request, template, context)
