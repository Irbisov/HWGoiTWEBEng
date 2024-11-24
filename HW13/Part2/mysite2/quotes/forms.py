from django import forms
from django.contrib.auth.models import User
from .models import Author, Quote, Tag


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Підтвердження пароля")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Паролі не співпадають.")

        # Валідація на складність пароля
        if len(password) < 8:
            raise forms.ValidationError("Пароль має бути не менше 8 символів.")
        if password.isdigit():
            raise forms.ValidationError("Пароль не може складатися лише з цифр.")
        if password.isalpha():
            raise forms.ValidationError("Пароль має містити як літери, так і цифри.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']


class QuoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Теги"
    )

    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']
        labels = {
            'text': 'Цитата',
            'author': 'Автор',
            'tags': 'Теги'
        }

