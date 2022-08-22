from django.contrib import admin

from .models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingList, Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Доступ к модели тегов.
    """
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_display_links = ('name', 'slug')
    search_fields = ('id', 'name')
    list_filter = ('slug',)
    ordering = ('id', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Доступ к модели ингридиентов.
    """
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


class RecipeIngredientInLine(admin.TabularInline):
    """
    Доступ к модели ингридиентов в рецепте на странице модели рецептов.
    """
    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    """
    Доступ к модели ингридиентов в рецепте.
    """
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_display_links = ('recipe',)
    list_filter = ('recipe',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Доступ к модели рецептов.
    """
    list_display = (
        'id',
        'name',
        'author',
        'count_favorite',
    )
    list_display_links = ('name',)
    list_filter = ('author', 'tags',)
    readonly_fields = ('count_favorite',)
    inlines = (RecipeIngredientInLine,)
    empty_value_display = '-пусто-'

    def count_favorite(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    count_favorite.short_description = 'В избранном'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """
    Доступ к модели рецептов в избранном списке пользователя.
    """
    list_display = ('user', 'recipe')
    list_filter = ('recipe',)
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """
    Доступ к модели списка покупок пользователя.
    """
    list_display = ('user', 'recipe')
    list_filter = ('recipe',)
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )
