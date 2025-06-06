from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models
from . import forms


class MainPage(ListView):
    """
    Главная страница со списком всех рецептов.
    """
    paginate_by = 15
    model = models.Recipiec
    template_name = 'recipiec/main_page.html'
    context_object_name = 'recipes'


class CatPage(ListView):
    """
    Страница категории, отображает рецепты выбранной категории.
    """
    paginate_by = 15
    model = models.Recipiec
    template_name = 'recipiec/cat_page.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Добавляет название категории в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['cat_name'] = models.Category.objects.get(id=self.kwargs['cat_id']).title
        return context

    def get_queryset(self):
        """
        Возвращает только рецепты выбранной категории.
        """
        return models.Recipiec.objects.filter(category__id=self.kwargs['cat_id'])


class RecipePage(DetailView):
    """
    Страница рецепта.
    """
    model = models.Recipiec
    template_name = 'recipiec/recipe.html'
    context_object_name = 'recipe'

    def get(self, request, *args, **kwargs):
        """
        Увеличивает счетчик просмотров при каждом посещении страницы.
        """
        self.object = self.get_object()
        self.object.count_views += 1
        self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Добавляет список ингредиентов в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['ingredients'] = models.Ingredients.objects.filter(recipe__id=self.object.id)
        return context


@login_required
def add_to_favorites(request, pk):
    """
    Добавляет рецепт в избранное для текущего пользователя.
    Доступно только авторизованным пользователям
    """
    recipe = get_object_or_404(models.Recipiec, pk=pk)
    # Проверяем, нет ли уже этого рецепта в избранном
    if not models.Favourites.objects.filter(recipe=recipe, creator=request.user).exists():
        models.Favourites.objects.create(recipe=recipe, creator=request.user)
    return redirect('recipe', pk=pk)


@login_required
def delete_favorites(request, pk):
    """
    Удаляет рецепт из избранного для текущего пользователя.
    Доступно только авторизованным пользователям
    """
    models.Favourites.objects.filter(
        recipe_id=pk,
        creator=request.user
    ).delete()
    return redirect('recipe', pk=pk)


@login_required
def delete_recipe(request, pk):
    """
    Удаляет рецепт (доступно только автору рецепта).
    """
    recipe = get_object_or_404(models.Recipiec, pk=pk)
    recipe.delete()
    return redirect('profile', pk=request.user.pk)


class ProfilePageView(LoginRequiredMixin, ListView):
    """
    Страница профиля пользователя со списком добавленных им рецептов.
    Доступно только авторизованным пользователям
    """
    model = models.Recipiec
    template_name = 'recipiec/profile.html'
    login_url = 'auth'
    context_object_name = 'recipe'

    def get_queryset(self):
        """
        Возвращает только те рецепты, которые были добавлены текущим пользователем.
        """
        return models.Recipiec.objects.filter(creator__id=self.request.user.pk)


class FavRecipePageView(LoginRequiredMixin, ListView):
    """
    Страница с избранными рецептами пользователя.
    """
    model = models.Favourites
    template_name = 'recipiec/fav_recipes.html'
    login_url = 'auth'
    context_object_name = 'recipe'

    def get_queryset(self):
        """
        Возвращает только те рецепты, которые были добавлены в избранное текущим пользователем.
        """
        return models.Favourites.objects.filter(creator__id=self.request.user.pk)


def user_logout(request):
    """
    Выход пользователя из системы.
    """
    logout(request)
    return redirect('main')


class LoginUserView(LoginView):
    """
    Класс-представление для авторизации пользователей.
    Использует кастомную форму forms.LoginUserForm.
    """
    form_class = forms.LoginUserForm
    template_name = 'recipiec/auth.html'
    success_url = 'main'


class RegUserView(CreateView):
    """
    Класс-представление для регистрации новых пользователей.
    Автоматически авторизует пользователя после успешной регистрации.
    """
    form_class = forms.RegUserForm
    template_name = 'recipiec/reg.html'

    def form_valid(self, form):
        """
        Обработка успешной регистрации: Сохраняет пользователя, затем
        авторизует его и перенаправляет на главную страницу
        """
        user = form.save()
        login(self.request, user)
        return redirect('main')


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-представление для создания нового рецепта.
    Использует формсет для добавления ингредиентов.
    """
    model = models.Recipiec
    form_class = forms.AddRecipeForm
    template_name = 'recipiec/create_recipe.html'

    def get_success_url(self):
        """
        Возвращает URL созданного рецепта после успешного сохранения.
        """
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        """
        Добавляет формсет ингредиентов в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = self.ingredient_formset(self.request.POST, prefix='ingredients')
        else:
            context['ingredient_formset'] = self.ingredient_formset(queryset=models.Ingredients.objects.none(), prefix='ingredients')
        return context

    def form_valid(self, form):
        """
        Обработка валидной формы:
        1. Сохраняет рецепт с привязкой к текущему пользователю
        2. Обрабатывает формсет ингредиентов
        3. Сохраняет связи ManyToMany
        """
        # Привязываем рецепт к текущему пользователю
        recipe = form.save(commit=False)
        recipe.creator = self.request.user
        recipe.save()
        form.save_m2m()  # Сохраняем ManyToMany (категории)

        # Обрабатываем формсет ингредиентов
        ingredient_formset = self.ingredient_formset(self.request.POST, prefix='ingredients')
        if ingredient_formset.is_valid():
            instances = ingredient_formset.save(commit=False)
            for instance in instances:
                instance.recipe = recipe
                instance.save()
            # Удаляем отмеченные для удаления ингредиенты
            for obj in ingredient_formset.deleted_objects:
                obj.delete()

        return redirect('recipe', pk=recipe.id)

    @property
    def ingredient_formset(self):
        """
        Создает и возвращает формсет для ингредиентов.
        Позволяет добавлять/удалять ингредиенты при создании рецепта.
        """
        return inlineformset_factory(
            parent_model=models.Recipiec,
            model=models.Ingredients,
            fields=('title', 'count'),
            extra=1,
            can_delete=True
        )