from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    email_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username


class Recipe(models.Model):

    DIFFICULTY = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]

    CATEGORY = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('dessert', 'Десерт'),
        ('drink', 'Напиток'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY
    )

    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True
    )

    ingredients = models.TextField()
    instructions = models.TextField()

    prep_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    servings = models.IntegerField(default=1)

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY,
        default='medium'
    )

    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title


class RecipeLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'recipe')


class RecipeFavorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"


class EmailVerification(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    token = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username