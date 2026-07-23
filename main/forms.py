from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re


class SimpleUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-group',
            'placeholder': 'Минимум 8 символов',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-group',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-group',
                'placeholder': 'Имя пользователя (3+ символов)',
                'autocomplete': 'username'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Это имя пользователя уже занято.')
        if len(username) < 3:
            raise ValidationError('Имя должно содержать минимум 3 символа.')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Используйте только буквы, цифры и подчёркивание.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        if not re.search(r'[0-9]', password1):
            raise ValidationError('Пароль должен содержать цифры.')
        if not re.search(r'[a-zA-Z]', password1):
            raise ValidationError('Пароль должен содержать буквы.')
        try:
            validate_password(password1)
        except ValidationError as e:
            raise ValidationError(str(e))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-group',
            'placeholder': 'Имя пользователя',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-group',
            'placeholder': 'Пароль',
            'autocomplete': 'current-password'
        })
    )


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Ваше имя'})
    )
    avatar = forms.FileField(
        required=False,
        label='Аватар',
        widget=forms.FileInput(attrs={'class': 'form-group', 'accept': 'image/*'})
    )

    class Meta:
        from .models import UserProfile
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-group',
                'placeholder': 'Расскажите о себе...',
                'rows': 4
            })
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        from .models import Recipe
        model = Recipe
        fields = ['title', 'description', 'category', 'image', 'ingredients', 'instructions', 
                  'prep_time', 'cook_time', 'servings', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Например: Паста Карбонара'}),
            'description': forms.Textarea(attrs={'class': 'form-group', 'rows': 3, 'placeholder': 'Опишите ваш рецепт: история, особенности, рекомендации...'}),
            'category': forms.Select(attrs={'class': 'form-group'}),
            'image': forms.FileInput(attrs={'class': 'form-group', 'accept': 'image/*'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-group', 'rows': 6, 'placeholder': 'Каждый ингредиент на новой строке\nПример:\n2 яйца\n100г спагетти\n50г бекона'}),
            'instructions': forms.Textarea(attrs={'class': 'form-group', 'rows': 8, 'placeholder': 'Каждый шаг на новой строке\nПример:\nСварите спагетти\nОбжарьте бекон\nСмешайте ингредиенты'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Минуты', 'min': '0', 'value': '0'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Минуты', 'min': '0', 'value': '0'}),
            'servings': forms.NumberInput(attrs={'class': 'form-group', 'min': '1', 'value': '1'}),
            'difficulty': forms.Select(attrs={'class': 'form-group'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        prep_time = cleaned_data.get('prep_time')
        cook_time = cleaned_data.get('cook_time')
        servings = cleaned_data.get('servings')
        
        if prep_time is None or prep_time < 0:
            self.add_error('prep_time', 'Время подготовки должно быть 0 или больше')
        if cook_time is None or cook_time < 0:
            self.add_error('cook_time', 'Время готовки должно быть 0 или больше')
        if servings is None or servings < 1:
            self.add_error('servings', 'Количество порций должно быть минимум 1')
        
        return cleaned_data
