from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views import View

from .forms import CommentForm


class CommentCreateView(View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = CommentForm(request.POST)
        ct = ContentType.objects.get(model=kwargs["content_type"])
        model = ct.model_class().objects.get(pk=kwargs["object_id"])
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user.profile
            new_comment.text = form.cleaned_data["text"]
            new_comment.content_object = model
            new_comment.save()
            return redirect(model.get_absolute_url())
        messages.add_message(request, messages.ERROR, "Не удалось оставить комментарий")
        return redirect(model.get_absolute_url())
