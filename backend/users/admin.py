from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    list_display_links = ('username', 'email')
    search_fields = ('username', 'role')
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_display_links = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('author',)
    empty_value_display = '-пусто-'
