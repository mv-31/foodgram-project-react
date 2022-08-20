from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from foodgram.paginators import PageLimitPagination
from .filters import IngredientFilter, RecipeFilter
from .models import (Tag, Ingredient, Recipe, FavoriteRecipe,
                     ShoppingList, RecipeIngredient)
from .permissions import AuthorOrReadOnly, AdminOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeShowSerializer,
                          RecipeListSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работа с тэгами.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работа с ингредиентами.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Работа с рецептами.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeShowSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeShowSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(FavoriteRecipe, request, pk)
        return self.delete_recipe(FavoriteRecipe, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingList, request, pk)
        return self.delete_recipe(ShoppingList, request, pk)

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(recipe=recipe,
                                user=request.user).exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        model.objects.create(recipe=recipe, user=request.user)
        serializer = RecipeListSerializer(recipe)
        return Response(data=serializer.data, status=HTTPStatus.CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(user=request.user,
                                recipe=recipe).exists():
            model.objects.filter(user=request.user,
                                 recipe=recipe).delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        file_name = f'{user.username}_shopping_list.txt'
        if not user.shopping_user.exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_recipe__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(amount=Sum('amount')).order_by('ingredient__name')
        response = HttpResponse(
            content_type='text/plain',
            charset='utf-8',
        )
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        response.write('Список продуктов к покупке:\r\n')
        for ingredient in ingredients:
            response.write(
                f'{ingredient["ingredient__name"]} '
                f'- {ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\r\n'
            )
        return response
