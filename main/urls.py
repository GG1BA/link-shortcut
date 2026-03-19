from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all_links, name='all_links'),
    path('stats/<str:short_code>/', views.link_stats, name='link_stats'),
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),
]