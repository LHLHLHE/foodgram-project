from django.http import Http404
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    PasswordSerializer
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    IngredientRecipe,
    TagRecipe,
    Favorite,
    ShoppingCart
)
from users.models import CustomUser, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Follow.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        return False


class CustomPasswordSerializer(PasswordSerializer):
    current_password = serializers.CharField(required=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')
        required_fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipePostSerializer(many=True)
    tags = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())
    )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        required_fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            TagRecipe.objects.create(
                tag=tag,
                recipe=recipe
            )

        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient.get('id')
                ),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()

        TagRecipe.objects.filter(recipe=instance).delete()
        for tag in tags:
            TagRecipe.objects.create(
                tag=get_object_or_404(
                    Tag,
                    id=tag.id),
                recipe=instance
            )

        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.filter(recipe=instance).create(
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient.get('id')
                ),
                amount=ingredient.get('amount'),
                recipe=instance
            )
        return instance

class IngredientInRecipeGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeGetSerializer(
        many=True,
        source='ingredient'
    )
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user.id,
            favorite_recipe_id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user.id,
            recipe_id=obj.id
        ).exists()


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='author.email',
        read_only=True
    )
    id = serializers.IntegerField(
        source='author.id',
        read_only=True,
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
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def validate(self, data):
        user = CustomUser.objects.get(id=self.context['request'].user.id)
        author = CustomUser.objects.get(id=self.context['author_id'])
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора!')
        return data

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user = self.context['request'].user,
            author=obj.author
            ).exists()

    def get_recipes(self, obj):
        return Recipe.objects.filter(author=obj.author)


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='favorite_recipe.id',
        read_only=True
    )
    name = serializers.CharField(
        source='favorite_recipe.name',
        read_only=True
    )
    image = serializers.CharField(
        source='favorite_recipe.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='favorite_recipe.cooking_time',
        read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = CustomUser.objects.get(id=self.context['request'].user.id)
        favorite_recipe = Recipe.objects.get(id=self.context['recipe_id'])
        if Favorite.objects.filter(
                user=user,
                favorite_recipe=favorite_recipe
        ).exists():
            raise serializers.ValidationError(
                'Этот товар уже есть у вас в избранном!')
        return data


class ShoppingCartCreateDestroySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.CharField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = CustomUser.objects.get(id=self.context['request'].user.id)
        recipe = Recipe.objects.get(id=self.context['recipe_id'])
        if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                'Этот товар уже есть в вашем списке покупок!')
        return data
