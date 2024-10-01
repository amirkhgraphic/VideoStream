from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User


class UserListAPIViewTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )

        # Obtain JWT token for the test user
        url = reverse('token_obtain_pair')  # JWT token obtain URL
        response = self.client.post(url, {
            'email': self.user.email,
            'password': 'testpassword123'
        })
        self.token = response.data['access']

    def test_user_list_authenticated(self):
        # Use the token to authenticate the request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('users-list')  # UserListAPIView URL
        response = self.client.get(url)

        # Check if the request was successful and returned the correct status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_user_list_unauthenticated(self):
        # Test access without authentication
        url = reverse('users-list')
        response = self.client.get(url)

        # Check if it returns 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
