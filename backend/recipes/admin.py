from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag, TagsRecipe)


class RecipeIngredientInLine(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1


class TagsRecipeInline(admin.TabularInline):
    model = TagsRecipe


@admin.register(TagsRecipe)
class TagsRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, TagsRecipeInline)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    list_filter = ("name",)


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
