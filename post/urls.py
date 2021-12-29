from django.urls import path

from .views import BaseView, PostDetailView

app_name = 'post'
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('post_detail/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
]
