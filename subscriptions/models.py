from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.plan and self.plan.duration_days:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.plan.name}"
