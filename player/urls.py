from django.urls import path
from .views import VideoListAPIView, VideoDetailAPIView, VideoViewerAPIView, VideoUploadView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('videos/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:pk>/', VideoDetailAPIView.as_view(), name='video-detail'),
    path('video/<int:video_id>/viewers/', VideoViewerAPIView.as_view(), name='video-viewers'),
]
