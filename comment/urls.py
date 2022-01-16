from django.urls import path

from .views import CommentCreateView

app_name = 'comment'
urlpatterns = [
    path('create/<str:content_type>/<int:object_id>/', CommentCreateView.as_view(), name='comment-create')
]
