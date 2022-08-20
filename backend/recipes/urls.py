from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
app_name = 'recipes'

router.register('tags',
                views.TagViewSet,
                basename='tag'
                )
router.register('ingredients',
                views.IngredientViewSet,
                basename='ingredient'
                )
router.register('recipes',
                views.RecipeViewSet,
                basename='recipe'
                )


urlpatterns = [
    path('', include(router.urls)),
]
