from django.contrib import admin
from .models import UserProfile, Recipe, RecipeLike, EmailVerification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_verified', 'created_at']
    list_filter = ['email_verified', 'created_at']
    search_fields = ['user__username']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'difficulty', 'views', 'likes', 'created_at']
    list_filter = ['difficulty', 'created_at', 'author']
    search_fields = ['title', 'description']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'author', 'image')
        }),
        ('Ингредиенты и инструкции', {
            'fields': ('ingredients', 'instructions')
        }),
        ('Параметры рецепта', {
            'fields': ('prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Статистика', {
            'fields': ('views', 'likes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(RecipeLike)
class RecipeLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'recipe__title']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['user__username']
