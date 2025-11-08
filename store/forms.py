from django import forms
from .models import Product


class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, label='Количество', initial=1)
