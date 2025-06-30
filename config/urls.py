from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.shortcuts import render


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', include("rooms.urls", namespace="rooms")),
    path('api/v1/', include("api.urls", namespace="api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
