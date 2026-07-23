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