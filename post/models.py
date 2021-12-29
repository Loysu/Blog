from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize


class Post(models.Model):
    """Отдельная статья"""
    title = models.CharField(max_length=127, verbose_name='Название', db_index=True, unique=True)
    description = models.CharField(max_length=511, verbose_name='Описание поста', blank=True)
    image_thumbnail = ProcessedImageField(
        upload_to='pictures',
        blank=True,
        processors=[SmartResize(600, 400)],
        format='JPEG',
        options={'quality': 60}
    )
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField('Tag', verbose_name='Tags')
    author = models.ForeignKey('Profile', verbose_name='Автор', on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name='Содержание')
    description_for_search_engines = models.CharField(max_length=511, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.description_for_search_engines:
            self.description_for_search_engines = self.description
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-pub_date',)


class Tag(models.Model):
    """Категории статей"""
    name = models.CharField(max_length=100, verbose_name='Имя tag\'а', db_index=True)
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.CharField(max_length=511, verbose_name='Краткая информация об авторе', blank=True)
    avatar_thumbnail = ProcessedImageField(
        upload_to='avatars',
        processors=[SmartResize(300, 300)],
        options={'quality': 60},
        default='avatars/default-avatar.jpg',
        blank=True,
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.user.username
        super().save(*args, **kwargs)
