from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'upload_date']
        read_only_fields = ['uploaded_at']
