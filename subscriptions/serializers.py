from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_days',
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'plan',
            'start_date',
            'end_date',
            'active',
        ]


class UserSubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'plan',
            'start_date',
            'end_date',
            'active',
        ]
        read_only_fields = [
            'user',
            'start_date',
            'end_date',
        ]
