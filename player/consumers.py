import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    viewers = {}

    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.group_name = f'video_{self.video_id}'

        VideoConsumer.viewers[self.video_id] = VideoConsumer.viewers.get(self.video_id, 0) + 1

        # Add the client to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Send the current viewer count to the new client
        await self.send_viewer_count()

        # Broadcast the viewer count to all clients in this video group
        await self.broadcast_viewer_count()

    async def disconnect(self, close_code):
        # Decrement the viewer count for this video
        if self.video_id in VideoConsumer.viewers:
            VideoConsumer.viewers[self.video_id] -= 1
            if VideoConsumer.viewers[self.video_id] <= 0:
                del VideoConsumer.viewers[self.video_id]

        # Remove the client from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        # Broadcast the updated viewer count to all clients in this video group
        await self.broadcast_viewer_count()

    async def send_viewer_count(self):
        # Send the viewer count for this video to the current client
        viewer_count = VideoConsumer.viewers.get(self.video_id, 0)
        await self.send(text_data=json.dumps({
            'viewers': viewer_count
        }))

    async def broadcast_viewer_count(self):
        # Broadcast the viewer count to all connected clients in this video group
        viewer_count = VideoConsumer.viewers.get(self.video_id, 0)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_viewer_count_to_all',
                'viewers': viewer_count
            }
        )

    async def send_viewer_count_to_all(self, event):
        # Send the viewer count to all clients in the group
        await self.send(text_data=json.dumps({
            'viewers': event['viewers']
        }))
