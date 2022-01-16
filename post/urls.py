from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import (
    BaseView,
    PostDetailView,
    TagDetailView,
    LoginView,
    RegistrationView,
    ProfileView,
    EditProfileView,
    CreatePostView,
    EditPostView,
    ChangeProfilePictureView,
)

app_name = 'post'
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('post_detail/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('tag_detail/<slug:slug>', TagDetailView.as_view(), name='tag_detail'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('post:base')), name='logout'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('profile/<slug:slug>', ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/edit', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<slug:slug>/change_picture', ChangeProfilePictureView.as_view(), name='change_picture'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('edit_post/<slug:slug>', EditPostView.as_view(), name='edit_post'),
]
