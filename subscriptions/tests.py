from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from subscriptions.models import SubscriptionPlan, UserSubscription

User = get_user_model()


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )

        self.plan1 = SubscriptionPlan.objects.create(
            name="Basic Plan", description="Basic Subscription", price=9.99, duration_days=30
        )
        self.plan2 = SubscriptionPlan.objects.create(
            name="Premium Plan", description="Premium Subscription", price=19.99, duration_days=60
        )

        token_url = reverse('users:token_obtain_pair')
        response = self.client.post(token_url, {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        })
        self.token = response.data['access']

    def test_list_subscription_plans(self):
        url = reverse('subscription:subscription-plans')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Basic Plan")
        self.assertEqual(response.data[1]['name'], "Premium Plan")

    def test_subscribe_to_plan(self):
        url = reverse('subscription:subscribe')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {'plan_id': self.plan1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        subscription = UserSubscription.objects.get(user=self.user)
        self.assertEqual(subscription.plan.name, 'Basic Plan')

    def test_check_user_subscription(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('subscription:subscribe')
        self.client.post(url, {'plan_id': self.plan1.id})

        url = reverse('subscription:user-subscription')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['plan'], self.plan1.id)
        self.assertEqual(response.data['user'], self.user.id)

    def test_user_subscription_without_auth(self):
        url = reverse('subscription:user-subscription')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
