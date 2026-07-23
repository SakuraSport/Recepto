from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import SimpleUserCreationForm, LoginForm, ProfileEditForm, RecipeForm
from .models import UserProfile, Recipe, RecipeLike


def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')[:12]
    
    # Add is_liked info for each recipe if user is authenticated
    if request.user.is_authenticated:
        liked_recipe_ids = set(
            RecipeLike.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )
        for recipe in recipes:
            recipe.is_liked = recipe.id in liked_recipe_ids
    else:
        for recipe in recipes:
            recipe.is_liked = False
    
    return render(request, 'main/index.html', {'recipes': recipes})


def add_recipe(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, '✅ Рецепт опубликован!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'main/add_recipe.html', {'form': form})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.views += 1
    recipe.save(update_fields=['views'])
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = RecipeLike.objects.filter(user=request.user, recipe=recipe).exists()
    
    context = {
        'recipe': recipe,
        'is_liked': is_liked,
        'ingredients': recipe.get_ingredients_list(),
        'instructions': recipe.get_instructions_list(),
        'total_time': recipe.get_total_time(),
    }
    return render(request, 'main/recipe_detail.html', context)


def recipes_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    
    recipes = Recipe.objects.all()
    
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        )
    
    if category:
        recipes = recipes.filter(category=category)
    
    recipes = recipes.order_by('-created_at')
    
    # Add is_liked info for each recipe if user is authenticated
    if request.user.is_authenticated:
        liked_recipe_ids = set(
            RecipeLike.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )
        for recipe in recipes:
            recipe.is_liked = recipe.id in liked_recipe_ids
    else:
        for recipe in recipes:
            recipe.is_liked = False
    
    context = {
        'recipes': recipes,
        'search_query': query,
        'selected_category': category,
        'categories': Recipe.CATEGORY_CHOICES,
    }
    return render(request, 'main/recipes_list.html', context)


def favorites(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    liked_recipes = Recipe.objects.filter(recipelike__user=request.user)
    return render(request, 'main/favorites.html', {'recipes': liked_recipes})


def toggle_like(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    recipe = get_object_or_404(Recipe, id=recipe_id)
    like, created = RecipeLike.objects.get_or_create(user=request.user, recipe=recipe)
    
    if not created:
        recipe.likes -= 1
        like.delete()
    else:
        recipe.likes += 1
    
    recipe.save(update_fields=['likes'])
    return redirect('recipe_detail', recipe_id=recipe_id)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, email_verified=True)
            messages.success(request, f'✅ Аккаунт создан! Добро пожаловать, {user.username}!')
            auth_login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SimpleUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'👋 Добро пожаловать, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, '❌ Неправильное имя пользователя или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'main/login.html', {'form': form})


@login_required(login_url='login')
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_recipes = request.user.recipes.all()
    
    context = {
        'profile': profile,
        'recipes': user_recipes,
    }
    return render(request, 'main/profile_new.html', context)


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if recipe.author != request.user:
        messages.error(request, '❌ Вы можете редактировать только свои рецепты!')
        return redirect('recipe_detail', recipe_id=recipe_id)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Рецепт обновлён!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'main/edit_recipe.html', {'form': form, 'recipe': recipe})


@login_required(login_url='login')
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if recipe.author != request.user:
        messages.error(request, '❌ Вы можете удалять только свои рецепты!')
        return redirect('recipe_detail', recipe_id=recipe_id)
    
    if request.method == 'POST':
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'✅ Рецепт "{recipe_title}" удалён!')
        return redirect('recipes_list')
    
    return render(request, 'main/delete_recipe.html', {'recipe': recipe})
