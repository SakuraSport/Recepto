from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    avatar = models.FileField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Profile'

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/default-avatar.png'


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]
    
    CATEGORY_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('dessert', 'Десерт'),
        ('drink', 'Напиток'),
        ('snack', 'Закуска'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lunch')
    image = models.FileField(
        upload_to='recipes/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    
    ingredients = models.TextField(help_text='Каждый ингредиент с новой строки')
    instructions = models.TextField(help_text='Пошаговые инструкции')
    
    prep_time = models.IntegerField(help_text='Время подготовки в минутах')
    cook_time = models.IntegerField(help_text='Время готовки в минутах')
    servings = models.IntegerField(help_text='Количество порций')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_total_time(self):
        return self.prep_time + self.cook_time

    def get_ingredients_list(self):
        return [item.strip() for item in self.ingredients.split('\n') if item.strip()]

    def get_instructions_list(self):
        return [item.strip() for item in self.instructions.split('\n') if item.strip()]


class RecipeLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} likes {self.recipe.title}'


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f'Email verification for {self.user.username}'
