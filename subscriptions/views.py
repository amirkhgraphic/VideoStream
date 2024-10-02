from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer, UserSubscriptionCreateSerializer

User = get_user_model()


class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer


class SubscribeView(generics.CreateAPIView):
    serializer_class = UserSubscriptionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            plan = SubscriptionPlan.objects.get(id=self.request.data['plan_id'])
        except SubscriptionPlan.DoesNotExist:
            raise ValidationError("The specified plan does not exist.")

        end_date = timezone.now() + timezone.timedelta(days=plan.duration_days)
        serializer.save(user=self.request.user, plan=plan, end_date=end_date)


class UserSubscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserSubscription.objects.filter(user=self.request.user).first()
