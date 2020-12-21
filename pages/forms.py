from django import forms
from .models import Comment
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CommentForm(forms.ModelForm):

    """Форма комментариев"""

    name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': "Имя",
                                      'class': 'form-control'})
    )
    email = forms.EmailField(
        label="",
        max_length=250,
        widget=forms.EmailInput(attrs={'placeholder': "E-mail",
                                       'class': 'form-control'})

    )
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Комментарий",
                                     'class': 'form-control',
                                     'rows': '3'}),
        required=True
    )

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')


class ContactForm(forms.Form):

    """Форма обратной связи"""

    name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': "Имя",
                                      'class': 'form-control'})
    )
    email = forms.EmailField(
        label="",
        max_length=250,
        widget=forms.EmailInput(attrs={'placeholder': "E-mail",
                                       'class': 'form-control'})
    )
    message = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Сообщение",
                                     'class': 'form-control',
                                     'rows': '3'}),
        required=True
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget(),
    )


class FuelCalculatorForm(forms.Form):

    """
    Считает средний расход топлива
    и
    показывает сколько литров еще можно долить.

    """

    litres = forms.DecimalField(
        label="Сколько литров потратил?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    overall_distance = forms.DecimalField(
        label="Сколько проехал?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    allowed_flow = forms.DecimalField(
        label="Какой расход установили в конторе?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "9 или 10",
                                        'class': 'form-control'}),
        required=False,
    )


class DistanceCalculatorForm(forms.Form):
    """
    Считает расстояние на которое хватит заправленного топлива

    """

    litres = forms.DecimalField(
        label="Сколько заправил?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    flow = forms.DecimalField(
        label="Какой расход?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    price_per_liter = forms.DecimalField(
        label="Сколько стоит литр?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
    )


class VolumeCalculatorForm(forms.Form):
    """
    Считает необходимый объем топлива на указанное расстояние

    """
    distance = forms.DecimalField(
        label="Какое расстояние?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    flow = forms.DecimalField(
        label="Какой расход?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    price_per_liter = forms.DecimalField(
        label="Сколько стоит литр?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )


class KFactorCalculatorForm(forms.Form):

    """Форма калькулятора К-фактора"""

    flow = forms.DecimalField(
        label="Максимальный расход Q",
        min_value=0,
        max_digits=11,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    freq = forms.DecimalField(
        label="Максимальная частота f",
        min_value=0,
        max_digits=11,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
