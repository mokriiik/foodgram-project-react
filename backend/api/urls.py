from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from api.views import (
    UserViewSet,
    RecipeViewSet,
    IngredientViewSet,
    TagViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'tags', TagViewSet, 'tags')
router.register(r'ingredients', IngredientViewSet, 'ingredients')
router.register(r'recipes', RecipeViewSet, 'recipes')

urlpatterns = (
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)