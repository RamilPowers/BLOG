from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    """Форма комментариев"""

    name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': "Представиться..."})
    )
    email = forms.EmailField(
        label="",
        max_length=250,
        widget=forms.EmailInput(attrs={'placeholder': "Написать E-mail..."})

    )
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Написать комментарий...",
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
        widget=forms.TextInput(attrs={'placeholder': "Представиться..."})
    )
    email = forms.EmailField(
        label="",
        max_length=250,
        widget=forms.EmailInput(attrs={'placeholder': "Написать E-mail..."})
    )
    message = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Написать сообщение...",
                                     'rows': '3'}),
        required=True
    )


class FuelCalculatorForm(forms.Form):

    """Форма калькулятора топлива"""

    division_price = forms.DecimalField(
        label="Цена одного деления, л",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "3.44"}),
        required=False,
        help_text="Необязатаельное поле",
    )
    divisions = forms.DecimalField(
        label="Сколько делений потратил?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "3..."}),
        required=False,
        help_text="Необязатаельное поле",
    )
    litres = forms.DecimalField(
        label="Сколько литров ушло на поездку?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "Дохуя..."}),
        required=False,
        help_text="Необязатаельное поле",
    )
    overall_distance = forms.DecimalField(
        label="А сколько проехал км?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "Может, и не дохуя..."}),
        required=True,
        help_text="Обязатаельное поле",
    )
    allowed_flow = forms.DecimalField(
        label="Сколько литров можно затратить на 100км?",
        min_value=0,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': "Обычно 9 или 10..."}),
        required=True,
        help_text="Обязатаельное поле",
    )


class KFactorCalculatorForm(forms.Form):

    """Форма калькулятора К-фактора"""

    flow = forms.DecimalField(
        label="Максимальный расход Q, т/ч (кг/ч)",
        min_value=0,
        max_digits=11,
        decimal_places=2,
        required=True,
        help_text="Обязательное поле",

    )
    freq = forms.DecimalField(
        label="Максимальная частота f, Гц",
        min_value=0,
        max_digits=11,
        decimal_places=2,
        required=True,
        help_text="Обязательное поле",
    )
