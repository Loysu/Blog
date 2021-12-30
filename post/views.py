from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate

from .models import Post, Tag, Profile
from .mixins import DefaultContextMixin
from .forms import LoginForm


class BaseView(DefaultContextMixin, ListView):
    """Основная страница"""
    model = Post
    template_name = 'post/base.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class PostDetailView(DefaultContextMixin, DetailView):
    """Отдельная статья"""
    model = Post

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class TagDetailView(DefaultContextMixin, DetailView):
    """Отдельный tag"""
    model = Tag
    context_object_name = 'main_tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        context['posts'] = Tag.objects.get(slug=context['main_tag'].slug).post_set.all()
        return context


class LoginView(View):
    """Аутентификация"""
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(self.request, 'post/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
            return redirect(reverse('post:base'))
        context = {
            'form': form,
        }
        return render(self.request, 'post/login.html', context)
