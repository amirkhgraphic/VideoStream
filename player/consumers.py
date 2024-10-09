import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from player.models import Video, VideoWatchHistory


class VideoConsumer(AsyncWebsocketConsumer):
    viewers = {}

    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.group_name = f'video_{self.video_id}'
        user = self.scope["user"]

        VideoConsumer.viewers[self.video_id] = VideoConsumer.viewers.get(self.video_id, 0) + 1

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        if user.is_authenticated:
            video = await database_sync_to_async(self.get_video)(self.video_id)
            await database_sync_to_async(self.create_watch_history)(user, video)

        await self.send_viewer_count()

        await self.broadcast_viewer_count()

    async def disconnect(self, close_code):
        if self.video_id in VideoConsumer.viewers:
            VideoConsumer.viewers[self.video_id] -= 1
            if VideoConsumer.viewers[self.video_id] <= 0:
                del VideoConsumer.viewers[self.video_id]

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        await self.broadcast_viewer_count()

    async def send_viewer_count(self):
        viewer_count = VideoConsumer.viewers.get(self.video_id, 0)
        await self.send(text_data=json.dumps({
            'viewers': viewer_count
        }))

    async def broadcast_viewer_count(self):
        viewer_count = VideoConsumer.viewers.get(self.video_id, 0)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_viewer_count_to_all',
                'viewers': viewer_count
            }
        )

    async def send_viewer_count_to_all(self, event):
        await self.send(text_data=json.dumps({
            'viewers': event['viewers']
        }))

    def get_video(self, video_id):
        return Video.objects.get(id=video_id)

    def create_watch_history(self, user, video):
        VideoWatchHistory.objects.create(user=user, video=video)
