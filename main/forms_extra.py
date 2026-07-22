from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Recipe


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
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-group',
                'placeholder': 'Расскажите о себе...',
                'rows': 4
            })
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'ingredients', 'instructions', 
                  'prep_time', 'cook_time', 'servings', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Название рецепта'}),
            'description': forms.Textarea(attrs={'class': 'form-group', 'rows': 3, 'placeholder': 'Краткое описание'}),
            'image': forms.FileInput(attrs={'class': 'form-group', 'accept': 'image/*'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-group', 'rows': 6, 'placeholder': 'Каждый ингредиент с новой строки'}),
            'instructions': forms.Textarea(attrs={'class': 'form-group', 'rows': 8, 'placeholder': 'Пошаговые инструкции'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Минуты'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': 'Минуты'}),
            'servings': forms.NumberInput(attrs={'class': 'form-group'}),
            'difficulty': forms.Select(attrs={'class': 'form-group'}),
        }
