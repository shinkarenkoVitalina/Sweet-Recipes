from django.contrib import admin
from . import models


class RecipiecAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'count_views')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'title', 'count')
    search_fields = ('recipe', 'title')
    list_filter = ('recipe',)


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'creator')
    search_fields = ('recipe', 'creator')


admin.site.register(models.Category)
admin.site.register(models.Recipiec, RecipiecAdmin)
admin.site.register(models.Favourites, FavouritesAdmin)
admin.site.register(models.Ingredients, IngredientsAdmin)
