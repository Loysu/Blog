from django.urls import path

from .views import (
    BaseView,
    PostDetailView,
    TagDetailView,
    LoginView
)

app_name = 'post'
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('post_detail/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('tag_detail/<slug:slug>', TagDetailView.as_view(), name='tag_detail'),
    path('login', LoginView.as_view(), name='login'),
]
