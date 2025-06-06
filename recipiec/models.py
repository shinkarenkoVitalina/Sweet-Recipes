from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Recipiec(models.Model):
    cooking_time = models.PositiveIntegerField(null=True, verbose_name="Время приготовления в минутах")
    description = models.TextField(verbose_name="Описание")
    title = models.CharField(max_length=255, verbose_name="Название")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="Фото")
    category = models.ManyToManyField(Category, verbose_name="Категория")
    count_views = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор рецепта")

    def formatted_cooking_time(self):
        hours = self.cooking_time // 60
        minutes = self.cooking_time % 60
        if hours and minutes:
            return f"{hours} ч. {minutes} мин."
        elif hours:
            return f"{hours} ч."
        else:
            return f"{minutes} мин."

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']

class Ingredients(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    count = models.CharField(max_length=128, verbose_name="Количество")
    recipe = models.ForeignKey(Recipiec, on_delete=models.CASCADE, verbose_name="Для рецепта")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Favourites(models.Model):
    recipe = models.ForeignKey(Recipiec, on_delete=models.CASCADE, verbose_name="Рецепт")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сохранен пользователем")

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
