from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, Tag, Profile
from .mixins import BaseContextMixin


class BaseView(BaseContextMixin, ListView):
    model = Post
    template_name = 'post/base.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class PostDetailView(BaseContextMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)

