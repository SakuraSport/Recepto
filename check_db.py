
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from main.models import Recipe, User

print(f"=== DATABASE CHECK ===")
print(f"Total recipes: {Recipe.objects.count()}")
print(f"Total users: {User.objects.count()}")

if Recipe.objects.exists():
    print("\nRecipes:")
    for recipe in Recipe.objects.all():
        print(f"  - {recipe.title} (by {recipe.author.username})")
else:
    print("\n❌ No recipes found!")

if User.objects.exists():
    print("\nUsers:")
    for user in User.objects.all():
        print(f"  - {user.username}")
