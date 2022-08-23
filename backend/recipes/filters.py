from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """
    Фильтр для ингридиентов.
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """
    Фильтр для рецептов.
    """
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    def favorite_filter(self, **kwargs):
        recipes = Recipe.objects.filter(
            favorite_recipe__user=self.request.user
        )
        return recipes

    def shopping_cart_filter(self, **kwargs):
        recipes = Recipe.objects.filter(
            shopping_recipe__user=self.request.user
        )
        return recipes

    class Meta:
        model = Recipe
        fields = ['author']
