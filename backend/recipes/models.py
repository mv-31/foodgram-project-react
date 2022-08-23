from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from foodgram import settings
from users.models import User


class Tag(models.Model):
    """
    Модель тегов.
    """
    name = models.CharField(
        max_length=40,
        unique=True,
        null=False,
        verbose_name='Название',
        help_text='Название тега',
    )
    color = ColorField(
        default="#000000",
        verbose_name='Цвета',
        help_text='Выберите цвет',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Введите слаг',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингридиентов.
    """
    name = models.CharField(
        verbose_name='Ингридиент',
        max_length=200,
        blank=False,
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
        blank=False,
        help_text='Единица измерения ингридиента',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='uniq_pair'
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель рецептов.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
        help_text='Название рецепта',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты рецепта',
        help_text='Ингредиенты рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        help_text='Теги',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Описание рецепта',
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='recipes/',
        help_text='Фото готового блюда',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            settings.MIN_COOKING_TIME,
            message='Время должно быть больше нуля!',
        )],
        verbose_name='Время приготовления',
        help_text='Время приготовления блюда',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель ингридиентов в рецепте.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            settings.MIN_AMOUNT_INGREDIENT,
            message='Количество должно быть больше нуля!',
        )],
        verbose_name='Количество',
        help_text='Количество ингредиента',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_exists'
            ),
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'


class FavoriteRecipe(models.Model):
    """
    Модель рецептов в избранном списке пользователя.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite_recipe',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite_user',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            ),
        ]
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class ShoppingList(models.Model):
    """
    Модель списка покупок пользователя.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_recipe'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_user',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shoppinglist',
            ),
        ]
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}: {self.recipe}'
