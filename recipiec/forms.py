from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class':'add-cat-input'})
        }


class AddRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = models.Recipiec
        fields = ['category', 'cooking_time', 'description', 'title', 'photo']
        widgets = {
            'category': forms.SelectMultiple(attrs={'class': 'change-cat-input'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'add-cooking_time-input'}),
            'description': forms.TextInput(attrs={'class': 'add-desc-input'}),
            'title': forms.TextInput(attrs={'class': 'add-title-recipe-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'add-photo-input'})
        }


class RegUserForm(UserCreationForm):
    username = forms.CharField(label='Введите имя', widget=forms.TextInput(attrs={'class': 'name-form'}))
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'pass-form'}))
    password2 = forms.CharField(label='Повторите введенный пароль', widget=forms.PasswordInput(attrs={'class': 'pass-form'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Введите имя', widget=forms.TextInput(attrs={'class': 'name-form'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'pass-form'}))
