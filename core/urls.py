from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include(('users.urls', 'users'), 'users')),
    path('api/subscription/', include(('subscriptions.urls', 'subscriptions'), 'subscription')),
    path('api/player/', include(('player.urls', 'player'), 'player')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
