from django.contrib import admin

from imagekit.admin import AdminThumbnail
from django_summernote.admin import SummernoteModelAdmin


from .models import Post, Tag, Profile


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """Пост"""
    summernote_fields = ('content',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author')
    list_editable = ('is_published',)
    list_display = ('title', 'author', 'pub_date', 'is_published')
    list_display_links = ('title',)
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги постов"""
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ('__str__',)
    admin_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')
