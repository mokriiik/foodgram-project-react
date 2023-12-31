from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from api.constants import MAX_LENGTH_COLOR, MAX_LENGTH_NAME

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        verbose_name="Название тега",
    )
    color = models.CharField(
        verbose_name="Цвет тега",
        max_length=MAX_LENGTH_COLOR,
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_NAME, unique=True, verbose_name="Слаг"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name="Название",
                            max_length=MAX_LENGTH_NAME)
    measurement_unit = models.CharField(
        verbose_name="Единица измерения", max_length=MAX_LENGTH_NAME
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(max_length=MAX_LENGTH_NAME,
                            verbose_name="Название")
    image = models.ImageField(
        verbose_name="Картинка"
    )
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        through_fields=("recipe", "ingredient"),
        related_name="recipes",
        blank=True,
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(Tag, through="TagsRecipe",
                                  related_name="recipes",
                                  verbose_name="Теги")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        default=0,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, verbose_name="Теги в рецепте", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт с тегами",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Тег в рецепте"
        verbose_name_plural = "Теги в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='Unique tag in recipe'
            )
        ]


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиенты в рецепте",
        related_name="ingredientsRecipes",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт с ингридиентами",
        related_name="ingredientsRecipes",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиентов",
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Количетсво ингредиентов в рецепте"
        verbose_name_plural = "Количетсво ингредиентов в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "ingredient"
                ),
                name="Unique Ingredients"
            )
        ]

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredient}"


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite_recipe",
        on_delete=models.CASCADE,
        verbose_name="Избранный рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Unique user in recipe'
            )
        ]

    def __str__(self):
        return f"{self.user} favorite {self.recipe}"


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="shopping_cart_recipe",
        on_delete=models.CASCADE,
        verbose_name="Рецепт в списке покупок",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="shopping_cart_user",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "user",
                ),
                name="Unique shopping cart"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.recipe}"
