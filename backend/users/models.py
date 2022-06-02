from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_user

ACCESS_LEVELS = (
    ('user', 'Авторизованный пользователь'),
    ('admin', 'Администратор')
)


class CustomUser(AbstractUser):
    '''
    Кастомная модель пользователя
    '''
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user],
        verbose_name='Логин',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Эл. почта'
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    access_level = models.CharField(
        max_length=150,
        choices=ACCESS_LEVELS,
        blank=True,
        default='user',
        verbose_name='Уровень доступа'
    )

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.access_level == 'admin'


class Follow(models.Model):
    '''
    Модель подписок
    '''
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique follow')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        default_related_name = 'follows'

    def __str__(self):
        return (
            f'user: {self.user.username}, '
            f'author: {self.author.username}'
        )
