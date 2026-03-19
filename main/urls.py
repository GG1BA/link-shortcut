from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all_links, name='all_links'),
    path('stats/<str:short_code>/', views.link_stats, name='link_stats'),
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),

    path('api/shorten', views.shorten_url_api, name='api_shorten'),
    path('api/<str:short_code>', views.URLRedirectAPIView.as_view(), name='api_redirect'),
    path('api/stats/<str:short_code>', views.URLStatsAPIView.as_view(), name='api_stats'),
]