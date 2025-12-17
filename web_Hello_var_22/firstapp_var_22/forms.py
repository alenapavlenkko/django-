from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Book, Author, Category, Publisher, Customer, Purchase, Review, BookAuthor

# === Форма для покупки книги пользователем ===
EXTRAS_CHOICES = [
    ('gift_wrap', 'Подарочная упаковка'),
    ('bookmark', 'Закладка'),
    ('signed_copy', 'Автограф автора'),
]

PAYMENT_CHOICES = [
    ('CARD', 'Банковская карта'),
    ('CASH', 'Наличные при получении'),
    ('ONLINE', 'Онлайн-оплата'),
]


class PurchaseBookForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    book_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    extras = forms.MultipleChoiceField(
        label='Дополнительно',
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=EXTRAS_CHOICES
    )
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=PAYMENT_CHOICES,
        initial='CARD',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


# === Форма редактирования книги (админка) ===
class BuyBookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label='Авторы'
    )

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название книги'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автоматически заполнится из названия'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '978-XXX-XXXXX-XX-X'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание книги'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'cover_type': forms.Select(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1000', 'max': '2100'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['authors'].initial = self.instance.authors.all()

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        if len(isbn) not in [10, 13]:
            raise ValidationError('ISBN должен содержать 10 или 13 символов')
        return isbn

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year in (None, ''):
            return None
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise ValidationError('Неверный формат года публикации.')
        current_year = timezone.now().year
        if year > current_year:
            raise ValidationError(f'Год публикации не может быть больше {current_year}.')
        if year < 1000:
            raise ValidationError('Год публикации должен быть не менее 1000.')
        return year

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError('Цена должна быть положительной')
        return price

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
        if 'authors' in self.cleaned_data:
            book.authors.clear()
            for author in self.cleaned_data['authors']:
                BookAuthor.objects.create(book=book, author=author)
        return book


# === Формы для остальных моделей ===
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя автора'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия автора'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Биография автора'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError('Дата рождения не может быть в будущем')
        return birth_date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автоматически заполнится из названия'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание категории'}),
        }


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название издательства'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Адрес издательства'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not any(char.isdigit() for char in phone):
            raise ValidationError('Телефон должен содержать цифры')
        return phone


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок отзыва'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш отзыв о книге'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

class PurchaseForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class':'form-control'}))
    book = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    extras = forms.MultipleChoiceField(
        required=False,
        choices=[('gift','Подарочная упаковка'), ('express','Экспресс-доставка')],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Purchase
        fields = ['payment_method', 'shipping_address', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Адрес доставки'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Дополнительные пожелания'}),
        }

    def clean_shipping_address(self):
        address = self.cleaned_data['shipping_address']
        if len(address.strip()) < 10:
            raise ValidationError('Адрес доставки должен быть более подробным')
        return address


class CustomerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш адрес'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not any(c.isdigit() for c in phone):
            raise ValidationError('Телефон должен содержать цифры')
        return phone
