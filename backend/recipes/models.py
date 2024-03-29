import textwrap

from django.core.validators import MinValueValidator
from django.db import models

from core.models import CreateModel
from users.models import CustomUser


class Tag(models.Model):
    '''
    Модель тэгов
    '''
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name='Идентификатор'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет в HEX'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return(
            f'name: {self.name}, '
            f'slug: {self.slug}, '
            f'color in HEX: {self.color}'
        )


class Ingredient(models.Model):
    '''
    Модель ингредиентов
    '''
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return(
            f'name: {self.name}, '
            f'measurement unit: {self.measurement_unit}'
        )


class Recipe(CreateModel):
    '''
    Модель рецептов
    '''
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тэги',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (
            f'name: {self.name}, '
            f'image URL: {self.image}, '
            f'description: {textwrap.shorten(self.text, width=15)}, '
            f'ingredients: {self.ingredients}, '
            f'tags: {self.tags}, '
            f'cooking time: {self.cooking_time}'
        )


class TagRecipe(models.Model):
    '''
    Модель связи тэгов и рецептов отношением многие-ко-многим
    '''
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag.slug} --- {self.recipe.name}'


class IngredientRecipe(models.Model):
    '''
    Модель связи ингредиентов и рецептов отношением многие-ко-многим
    '''
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.ingredient.name} --- {self.recipe.name}, {self.amount}'


class Favorite(models.Model):
    '''
    Модель избранного
    '''
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=('user', 'favorite_recipe'),
            name='unique favourite'
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return (
            f'user: {self.user.username}, '
            f'favourite recipe: {self.favorite_recipe.name}'
        )


class ShoppingCart(models.Model):
    '''
    Модель списка покупок
    '''
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='unique recipe in shopping cart'
        )
        verbose_name = 'Список покупок'

    def __str__(self):
        return (
            f'user: {self.user.username}, '
            f'recipe in shopping cart: {self.recipe.name}'
        )
