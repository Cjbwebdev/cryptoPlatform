# crypto_charts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.crypto_list, name='crypto_list'),
    path('chart-data/<str:crypto_id>/<str:time_frame>/', views.crypto_chart_data, name='crypto_chart_data'),
    path('article/<str:article_id>/', views.article_detail, name='article_detail'),
]
