from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views import View, generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.contrib import messages
from django.forms.models import model_to_dict

from .models import Post, Tag, Profile
from .mixins import DefaultContextMixin
from .forms import LoginForm, RegistrationForm, EditProfileForm


class BaseView(DefaultContextMixin, generic.ListView):
    """Основная страница"""
    model = Post
    template_name = 'post/base.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class PostDetailView(DefaultContextMixin, generic.DetailView):
    """Отдельная статья"""
    model = Post

    def get_context_data(self, **kwargs):
        return super().get_context_data(self.request, **kwargs)


class TagDetailView(DefaultContextMixin, generic.DetailView):
    """Отдельный tag"""
    model = Tag
    context_object_name = 'main_tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        context['posts'] = Tag.objects.get(slug=context['main_tag'].slug).post_set.all()
        return context


class LoginView(View):
    """Авторизация"""
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(self.request, 'post/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
            messages.success(
                self.request,
                f'Добро пожаловать, {user.first_name if user.first_name else user.username}!'
            )
            return redirect(reverse('post:base'))
        context = {
            'form': form,
        }
        return render(self.request, 'post/login.html', context)


class RegistrationView(View):
    """Регистрация"""
    def get(self, *args, **kwargs):
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(self.request, 'post/registration.html', context)

    def post(self, *args, **kwargs):
        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name'].title()
            new_user.last_name = form.cleaned_data['last_name'].title()
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                slug=slugify(new_user.username)
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(self.request, user)
            messages.success(
                self.request,
                f'Добро пожаловать, {user.first_name if user.first_name else user.username}! с:'
            )
            return redirect(reverse('post:base'))
        context = {
            'form': form,
        }
        return render(self.request, 'post/registration.html', context)


class ProfileView(DefaultContextMixin, generic.DetailView):
    """Подробная информация о пользователе"""
    model = Profile
    template_name_suffix = ''
    context_object_name = 'main_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        context['user'] = self.request.user
        context['articles'] = Profile.objects.get(user=context['main_profile'].user).post_set.order_by('pub_date')
        return context


class EditProfileView(View):
    """Настройки профиля"""
    def get(self, *args, **kwargs):
        if isinstance(self.request.user, AnonymousUser):
            messages.warning(self.request, 'У вас недостаточно прав!')
            return redirect(reverse('post:base'))
        elif Profile.objects.get(user=self.request.user) != Profile.objects.get(slug=kwargs['slug']):
            messages.warning(self.request, 'Вы можете редактировать только свой профиль!')
            return redirect(reverse('post:base'))
        profile = Profile.objects.get(slug=kwargs['slug'])
        data = model_to_dict(profile.user)
        data.update(bio=profile.bio)
        form = EditProfileForm(initial=data)
        context = {
            'profile': profile,
            'form': form,
        }
        return render(self.request, 'post/profile_settings.html', context)

    def post(self, *args, **kwargs):
        profile = Profile.objects.get(slug=kwargs['slug'])
        user = profile.user
        form = EditProfileForm(self.request.POST, user=user)
        if form.is_valid():
            User.objects.filter(pk=user.pk).update(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'].title(),
                last_name=form.cleaned_data['last_name'].title(),
            )
            user.set_password(form.cleaned_data['password'])
            user.save(update_fields=['password'])
            Profile.objects.filter(user=user).update(bio=form.cleaned_data['bio'])
            messages.success(
                self.request,
                f'Ваш профиль успешно обновлен с:'
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(self.request, user)
            return redirect(reverse('post:base'))
        context = {
            'profile': profile,
            'form': form,
        }
        return render(self.request, 'post/profile_settings.html', context)

