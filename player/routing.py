from django.urls import path

from .consumers import VideoConsumer

websocket_urlpatterns = [
    path('ws/video/<int:video_id>/', VideoConsumer.as_asgi()),
]
