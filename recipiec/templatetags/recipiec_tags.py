from django import template
from .. import models

register = template.Library()

@register.inclusion_tag('recipiec/list_cats.html')
def show_cats():
    """
        Возвращает список всех категорий рецептов для отображения в шаблоне.
    """
    cats = models.Category.objects.all()
    return {"categorys": cats}


@register.simple_tag()
def is_favorite(recipe, user):
    """
        Проверяет, добавлен ли рецепт в избранное у указанного пользователя.
        Возвращает True, если рецепт в избранном, иначе False.
    """
    return models.Favourites.objects.filter(recipe=recipe, creator=user).exists()


