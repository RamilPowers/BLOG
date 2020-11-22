# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, About
from django.views.generic import ListView
from .forms import CommentForm, ContactForm, FuelCalculatorForm, KFactorCalculatorForm
from django.core.mail import send_mail
from blog.settings import base


class PostListView(ListView):

    """Список всех постов"""

    queryset = Post.objects.filter(status="yes")
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'pages/post/list.html'


def get_post_detail(request, slug):

    """Детальный просмотр поста с комментариями"""

    posts = Post.objects.filter(status="yes")
    post = get_object_or_404(Post, status='yes', slug=slug)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm() 
    
    # Подборка окончаний для слова "Комментарий"
    if len(comments) % 10 == 1:
        pluralize = 'й'
    elif 2 <= len(comments) % 10 <= 4:
        if 10 < len(comments) < 20:
            pluralize = 'ев'
        else:
            pluralize = 'я'
    elif len(comments) % 10 > 4 or len(comments) % 10 == 0:
        pluralize = 'ев'  

    template = 'pages/post/detail.html'
    context = {
        'post': post,
        'posts': posts,
        'comments': comments,
        'comment_form': comment_form,
        'pluralize': pluralize,
    }
    return render(request, template, context)


def get_contact(request):

    """Просмотр контактной информации"""

    sent = False
    mail_from = base.EMAIL_HOST_USER
    mail_to = [base.EMAIL_HOST_USER]

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"Блог  - Новое письмо от {cd['name']}"
            message = f"Прислал: {cd['email']} \nВот текст сообщения: \n{cd['message']}"
            send_mail(subject, message, mail_from, mail_to)
            sent = True
    else:
        form = ContactForm()
    template = 'pages/contact.html'
    context = {
        'form': form,
        'sent': sent,
    }
    return render(request, template, context)


class AboutListView(ListView):

    """Просмотр страницы Резюме"""

    model = About
    queryset = About.objects.all()[:1]
    context_object_name = 'about'
    template_name = 'pages/about.html'


def get_fuel(request):

    """Посчитать кол-во топлива"""

    flow = None
    volume = None
    delta_volume = None
    if request.method == 'POST':
        form = FuelCalculatorForm(request.POST)
        if form.is_valid():
            overall_distance = form.cleaned_data['overall_distance']
            allowed_flow = form.cleaned_data['allowed_flow']
            if form.cleaned_data['division_price'] is None:
                # Если цена деления не задана, задается по умолчанию
                division_price = Decimal("3.44")
            else:
                # Иначе читается из формы
                division_price = form.cleaned_data['division_price']
            if form.cleaned_data['divisions']:
                # Если задано кол-во делений, высчитывается общий объем
                divisions = form.cleaned_data['divisions']
                litres = division_price * divisions
            else:
                # Иначе читается из формы
                litres = form.cleaned_data['litres']
            flow = round(litres * 100 / overall_distance, 1)
            volume = allowed_flow * overall_distance / 100
            delta_volume = round(volume - litres, 1)
    else:
        form = FuelCalculatorForm
    template = 'pages/fuel_calculator.html'
    context = {
        'form': form,
        'flow': flow,
        'volume': volume,
        'delta_volume': delta_volume,
    }
    return render(request, template, context)


def get_kfactor(request):

    """Вычислить К-фактор"""

    k_factor = None
    if request.method == 'POST':
        form = KFactorCalculatorForm(request.POST)
        if form.is_valid():
            flow = form.cleaned_data['flow']
            freq = form.cleaned_data['freq']
            k_factor = round(3600 * freq / flow, 3)
    else:
        form = KFactorCalculatorForm
    template = 'pages/kfactor_calculator.html'
    context = {
        'form': form,
        'k_factor': k_factor,
    }
    return render(request, template, context)