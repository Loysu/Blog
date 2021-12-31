from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import (
    BaseView,
    PostDetailView,
    TagDetailView,
    LoginView,
    RegistrationView,
)

app_name = 'post'
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('post_detail/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('tag_detail/<slug:slug>', TagDetailView.as_view(), name='tag_detail'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('post:base')), name='logout'),
    path('registration', RegistrationView.as_view(), name='registration'),
]
