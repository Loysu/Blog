from django.urls import re_path

from .consumers import CommentsConsumer

websocket_urlpatterns = [
    re_path(r"post_detail/(?P<post_id>\d+)/$", CommentsConsumer.as_asgi())
]
