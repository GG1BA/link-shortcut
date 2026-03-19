from django.urls import path
from . import views

urlpatterns = [
    path('api/shorten', views.shorten_url_api, name='api_shorten'),
    path('api/<str:short_code>', views.URLRedirectAPIView.as_view(), name='api_redirect'),
    path('api/stats/<str:short_code>', views.URLStatsAPIView.as_view(), name='api_stats'),
]