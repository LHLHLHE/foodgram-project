from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'access_level')
    search_fields = ('username', 'email', 'access_level')
    list_filter = ('username', 'email')


@admin.register(Follow)
class TagAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
