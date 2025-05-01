from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    # Admin page
    path(f'{settings.ADMIN_ROUTE}/', admin.site.urls),
    # API
    path('api/', include('api.urls')),
]
