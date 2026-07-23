from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .forms import RegisterForm, LoginForm, RecipeForm
from .models import Recipe, RecipeLike, UserProfile, RecipeFavorite


def home(request):
    recipes = Recipe.objects.all()[:12]

    return render(request, 'main/index.html', {
        'recipes': recipes
    })


@login_required
def add_recipe(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            messages.success(request, 'Рецепт добавлен')

            return redirect('home')

    else:
        form = RecipeForm()

    return render(request, 'main/add_recipe.html', {
        'form': form
    })



def recipe_detail(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    recipe.views += 1
    recipe.save()


    liked = False
    favorite = False


    if request.user.is_authenticated:

        liked = RecipeLike.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()


        favorite = RecipeFavorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()


    return render(request, 'main/recipe_detail.html', {
        'recipe': recipe,
        'liked': liked,
        'favorite': favorite,
        'ingredients': recipe.ingredients.split('\n'),
        'instructions': recipe.instructions.split('\n')
    })



def recipes_list(request):

    text = request.GET.get('q')

    recipes = Recipe.objects.all()


    if text:
        recipes = recipes.filter(
            Q(title__icontains=text) |
            Q(description__icontains=text)
        )


    return render(request, 'main/recipes_list.html', {
        'recipes': recipes
    })



@login_required
def toggle_like(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )


    like = RecipeLike.objects.filter(
        user=request.user,
        recipe=recipe
    )


    if like.exists():

        like.delete()
        recipe.likes -= 1

    else:

        RecipeLike.objects.create(
            user=request.user,
            recipe=recipe
        )

        recipe.likes += 1


    recipe.save()


    return redirect(
        'recipe_detail',
        recipe_id
    )



def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)


        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user
            )

            login(request, user)

            return redirect('home')


    else:

        form = RegisterForm()


    return render(request, 'main/register.html', {
        'form': form
    })



def user_login(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)


        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )


            if user:

                login(request, user)

                return redirect('home')


    else:

        form = LoginForm()


    return render(request, 'main/login.html', {
        'form': form
    })



@login_required
def profile(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    recipes = Recipe.objects.filter(
        author=request.user
    )


    return render(request, 'main/profile.html', {
        'profile': profile,
        'recipes': recipes
    })



@login_required
def edit_recipe(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )


    if request.method == 'POST':

        form = RecipeForm(
            request.POST,
            request.FILES,
            instance=recipe
        )


        if form.is_valid():

            form.save()

            return redirect(
                'recipe_detail',
                recipe_id
            )


    else:

        form = RecipeForm(
            instance=recipe
        )


    return render(request, 'main/edit_recipe.html', {
        'form': form
    })



@login_required
def toggle_favorite(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )


    favorite = RecipeFavorite.objects.filter(
        user=request.user,
        recipe=recipe
    )


    if favorite.exists():

        favorite.delete()

    else:

        RecipeFavorite.objects.create(
            user=request.user,
            recipe=recipe
        )


    return redirect(
        'recipe_detail',
        recipe_id
    )



@login_required
def favorites(request):

    recipes = Recipe.objects.filter(
        recipefavorite__user=request.user
    )


    return render(request, 'main/favorites.html', {
        'recipes': recipes
    })



def download_recipe_json(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )


    data = {
        'title': recipe.title,
        'author': recipe.author.username,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions
    }


    response = JsonResponse(data)

    response['Content-Disposition'] = (
        f'attachment; filename="{recipe.title}.json"'
    )


    return response



@login_required
def delete_recipe(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )


    if request.method == 'POST':

        recipe.delete()

        messages.success(
            request,
            'Рецепт удалён'
        )

        return redirect('home')


    return render(request, 'main/delete_recipe.html', {
        'recipe': recipe

    })
def user_profile(request):
    return profile(request)