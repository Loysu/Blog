from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, Tag, Profile
from .mixins import DefaultContextMixin


class BaseView(DefaultContextMixin, ListView):
    model = Post
    template_name = 'post/base.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class PostDetailView(DefaultContextMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class TagDetailView(DefaultContextMixin, DetailView):
    model = Tag
    context_object_name = 'main_tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        context['posts'] = Tag.objects.get(slug=context['main_tag'].slug).post_set.all()
        return context
