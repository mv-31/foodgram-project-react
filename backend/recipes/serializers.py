from django.core.validators import MinValueValidator
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Tag, Ingredient, RecipeIngredient, Recipe, FavoriteRecipe, ShoppingList
)
from users.models import Follow
from foodgram.settings import MIN_AMOUNT_INGREDIENT, MIN_COOKING_TIME
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов.
    """
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингридиентов.
    """
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(required=False)
    measurement_unit = serializers.CharField(required=False)
    amount = serializers.IntegerField(
        validators=(MinValueValidator(MIN_AMOUNT_INGREDIENT),)
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeCreateIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов при создании рецепта.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(
        validators=(MinValueValidator(MIN_AMOUNT_INGREDIENT),)
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецептов.
    """
    author = UserSerializer(
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = RecipeCreateIngredientSerializer(
        many=True,
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(MinValueValidator(MIN_COOKING_TIME),)
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        validators = (
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name',),
            ),
        )

    @staticmethod
    def create_ingredients(ingredients, recipe):
        """
        Создание ингридиентов для рецепта.
        """
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_id,
                amount=amount,
            )
            ingredient_list.append(recipe_ingredient)
        RecipeIngredient.objects.bulk_create(ingredient_list)

    @transaction.atomic
    def create(self, validated_data):
        """
        Создание рецепта.
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        """
        Редактирование рецепта.
        """
        recipe.ingredients.clear()
        recipe.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class RecipeShowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов.
    """
    author = UserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient',
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingList.objects.filter(user=user, recipe=obj).exists()


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов в подписке.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения подписки.
    """
    id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    email = serializers.CharField(
        source='author.email',
        read_only=True
    )
    username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True
    )
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes = obj.author.recipes.all()
        return RecipeListSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        subscribe = Follow.objects.filter(
            user=self.context.get('request').user,
            author=obj.author
        )
        if subscribe:
            return True
        return False

    @staticmethod
    def get_recipes_count(obj):
        return obj.author.recipes.count()
