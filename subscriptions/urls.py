from django.urls import path
from .views import SubscriptionPlanListView, SubscribeView, UserSubscriptionDetailView

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('me/', UserSubscriptionDetailView.as_view(), name='user-subscription'),
]
