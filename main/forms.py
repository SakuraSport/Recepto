from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Recipe


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя пользователя'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль'
        })
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'category',
            'image',
            'ingredients',
            'instructions',
            'prep_time',
            'cook_time',
            'servings',
            'difficulty'
        ]

    def clean_prep_time(self):
        value = self.cleaned_data.get('prep_time')
        if value is None:
            return 0
        if value < 0:
            raise forms.ValidationError('Время подготовки не может быть отрицательным.')
        return value

    def clean_cook_time(self):
        value = self.cleaned_data.get('cook_time')
        if value is None:
            return 0
        if value < 0:
            raise forms.ValidationError('Время готовки не может быть отрицательным.')
        return value

    def clean_servings(self):
        value = self.cleaned_data.get('servings')
        if value is None:
            return 1
        if value < 1:
            raise forms.ValidationError('Количество порций должно быть положительным числом (>=1).')
        return value