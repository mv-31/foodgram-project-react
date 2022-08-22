import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from foodgram import settings

USER = 'user'
ADMIN = 'admin'
IS_BLOCKED = 'is_blocked'


class User(AbstractUser):
    """
    Модель пользователей.
    """
    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN),
        (IS_BLOCKED, IS_BLOCKED),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Имя пользователя',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='email',
        help_text='email',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
        verbose_name='Роль',
        help_text='Права пользователя',
    )
    password = models.CharField(
        max_length=100,
        null=True,
        help_text='Пароль',
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_blocked(self):
        return self.role == self.IS_BLOCKED


class Follow(models.Model):
    """
    Модель подписок на пользователей.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='uniq_follow',
            ),
        ]
