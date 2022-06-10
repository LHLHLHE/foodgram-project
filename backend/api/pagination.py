from rest_framework.pagination import PageNumberPagination


class RecipesAndFollowsPagination(PageNumberPagination):
    page_size = 6
