import tempfile

from rest_framework.test import APITestCase
from rest_framework import status
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from django.urls import reverse
from django.test import TransactionTestCase

from .routing import websocket_urlpatterns
from .models import Video


class VideoListAPITest(APITestCase):
    def setUp(self):
        # Create a temporary video file for testing
        video_file = tempfile.NamedTemporaryFile(suffix=".mp4").name
        Video.objects.create(title="Test Video 1", video_file=video_file)
        Video.objects.create(title="Test Video 2", video_file=video_file)

    def test_get_video_list(self):
        url = reverse('player:video-list')  # Ensure this matches your URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class VideoDetailAPITest(APITestCase):
    def setUp(self):
        video_file = tempfile.NamedTemporaryFile(suffix=".mp4").name
        self.video = Video.objects.create(title="Test Video", video_file=video_file)

    def test_get_video_detail(self):
        url = reverse('player:video-detail', kwargs={'pk': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Video")


class VideoViewerCountAPITest(APITestCase):
    def setUp(self):
        video_file = tempfile.NamedTemporaryFile(suffix=".mp4").name
        self.video = Video.objects.create(title="Test Video", video_file=video_file)

    def test_get_video_viewer_count(self):
        url = reverse('player:video-viewers', kwargs={'video_id': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('viewer_count', response.data)
        # Assuming initial viewer count is simulated as 5
        self.assertEqual(response.data['viewer_count'], 0)


class WebSocketTestCase(TransactionTestCase):
    async def connect_and_receive(self, video_id):
        # Create a WebsocketCommunicator that connects to the video WebSocket
        communicator = WebsocketCommunicator(
            application=URLRouter(websocket_urlpatterns),
            path=f"/ws/videos/{video_id}/"
        )
        # Connect to the WebSocket
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Receive the first message (number of viewers)
        response = await communicator.receive_json_from()
        return response, communicator

    async def test_viewer_count(self):
        video_id = 1  # Assuming a video with ID 1

        # First WebSocket connection
        response, communicator1 = await self.connect_and_receive(video_id)
        self.assertEqual(response['viewer_count'], 1)

        # Second WebSocket connection
        response, communicator2 = await self.connect_and_receive(video_id)
        self.assertEqual(response['viewer_count'], 2)

        # Close second WebSocket connection
        await communicator2.disconnect()
        response = await communicator1.receive_json_from()
        self.assertEqual(response['viewer_count'], 1)

        # Close first WebSocket connection
        await communicator1.disconnect()
