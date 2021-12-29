from django.views.generic.base import ContextMixin

from .models import Post, Tag, Profile


class BaseContextMixin(ContextMixin):
    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=request.user)
        return context
