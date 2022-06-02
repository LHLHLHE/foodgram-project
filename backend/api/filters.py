from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag


class RecipesFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
