# crypto_platform/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crypto/', include('crypto_charts.urls')),  # Use the correct app name
]
