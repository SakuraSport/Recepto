from django import forms
from .models import UserProfile, Recipe


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Расскажите о себе...'
            }),
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*'
            })
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'image',
            'ingredients',
            'instructions',
            'prep_time',
            'cook_time',
            'servings',
            'difficulty'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название рецепта'
            }),

            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Описание'
            }),

            'ingredients': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Ингредиенты'
            }),

            'instructions': forms.Textarea(attrs={
                'rows': 7,
                'placeholder': 'Как приготовить'
            }),

            'image': forms.FileInput(attrs={
                'accept': 'image/*'
            })
        }