from django import forms
from .models import Product


class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, label='Количество', initial=1)


class OrderForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    adress = forms.CharField(label='Адрес доставки', widget=forms.Textarea)
    email = forms.EmailField(label='Email для подтверждения')
