# firstapp_var_22/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Book, Order, Review, OrderItem


class OrderForm(forms.Form):
    """Форма для оформления заказа"""
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    shipping_address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=Order.PAYMENT_METHODS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        label='Примечания',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )


class SimpleOrderForm(forms.Form):
    """Упрощенная форма для быстрой покупки"""
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш отзыв о книге'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Рейтинг должен быть от 1 до 5')
        return rating