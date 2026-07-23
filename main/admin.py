from django.contrib import admin
from .models import UserProfile, Recipe, RecipeLike, EmailVerification


admin.site.register(UserProfile)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "difficulty")


admin.site.register(RecipeLike)
admin.site.register(EmailVerification)