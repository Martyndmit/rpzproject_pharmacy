from django import forms
from .models import Order


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, max_value=50,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email',
            'delivery_method', 'city', 'address',
            'has_prescription', 'prescription_note'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select', 'id': 'id_delivery_method'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва міста'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адреса або номер відділення'}),
            'has_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prescription_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                        'placeholder': 'Опишіть рецепт або вкажіть спосіб його надання'}),
        }


class SymptomSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введіть симптом (наприклад: головний біль, кашель...)'
        })
    )
