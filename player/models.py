from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])]
    )
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VideoWatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='unique_user_video')
        ]

    def __str__(self):
        return f"{self.user} watched {self.video} at {self.watched_at}"
