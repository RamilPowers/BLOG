# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Comment, About
from django.views.generic import ListView
from .forms import CommentForm, ContactForm, \
    FuelCalculatorForm, KFactorCalculatorForm, \
    DistanceCalculatorForm, VolumeCalculatorForm
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
            return HttpResponseRedirect('#')
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
    distance = None
    sum = None
    litres = None
    total_litres = None

    if request.method == 'POST' and 'btn1' in request.POST:
        calc1_submit = True
        flow_form = FuelCalculatorForm(request.POST)
        if flow_form.is_valid():
            overall_distance = flow_form.cleaned_data['overall_distance']
            allowed_flow = flow_form.cleaned_data['allowed_flow']
            litres = flow_form.cleaned_data['litres']
            flow = round(litres * 100 / overall_distance, 1)
            if allowed_flow:
                volume = round(allowed_flow * overall_distance / 100, 1)
                delta_volume = round(volume - litres, 1)
            # return HttpResponseRedirect('#calc1')
    else:
        calc1_submit = False
        flow_form = FuelCalculatorForm

    if request.method == 'POST' and 'btn2' in request.POST:
        calc2_submit = True
        distance_form = DistanceCalculatorForm(request.POST)
        if distance_form.is_valid():
            litres = distance_form.cleaned_data['litres']
            flow = distance_form.cleaned_data['flow']
            distance = round(litres * 100 / flow, 1)
            price_per_liter = distance_form.cleaned_data['price_per_liter']
            if price_per_liter:
                sum = round(litres * price_per_liter)
    else:
        calc2_submit = False
        distance_form = DistanceCalculatorForm

    if request.method == 'POST' and 'btn3' in request.POST:
        calc3_submit = True
        volume_form = VolumeCalculatorForm(request.POST)
        if volume_form.is_valid():
            distance = volume_form.cleaned_data['distance']
            flow = volume_form.cleaned_data['flow']
            price_per_liter = volume_form.cleaned_data['price_per_liter']
            total_litres = round(flow * distance / 100, 1)
            sum = round(total_litres * price_per_liter, 1)
    else:
        calc3_submit = False
        volume_form = VolumeCalculatorForm


    template = 'pages/fuel_calculator.html'
    context = {
        'flow_form': flow_form,
        'distance_form': distance_form,
        'volume_form': volume_form,
        'flow': flow,
        'volume': volume,
        'delta_volume': delta_volume,
        'distance': distance,
        'total_litres': total_litres,
        'sum': sum,
        'litres': litres,
        'calc1_submit': calc1_submit,
        'calc2_submit': calc2_submit,
        'calc3_submit': calc3_submit,
    }
    return render(request, template, context)


def get_kfactor(request):

    """Вычислить К-фактор"""

    k_factor = None
    if request.method == 'POST':
        submit = True
        form = KFactorCalculatorForm(request.POST)
        if form.is_valid():
            flow = form.cleaned_data['flow']
            freq = form.cleaned_data['freq']
            k_factor = round(3600 * freq / flow, 3)
    else:
        submit = False
        form = KFactorCalculatorForm
    template = 'pages/kfactor_calculator.html'
    context = {
        'form': form,
        'k_factor': k_factor,
        'submit': submit,
    }
    return render(request, template, context)
