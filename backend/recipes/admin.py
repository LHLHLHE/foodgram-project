from django.contrib import admin


from .models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def recipe_in_favorites_count(self, obj):
        return Favorite.objects.filter(favorite_recipe=obj).count()

    recipe_in_favorites_count.short_description = 'In favorites count'
    list_display = ('name', 'author', 'recipe_in_favorites_count')
    list_filter = ('name', 'author__username', 'tags__name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
