from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from main.models import ShortURL

class BaseAPITestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.test_url_1 = ShortURL.objects.create(
            original_url="https://www.google.com",
            short_code="abc123",
            clicks=5
        )
        
        self.test_url_2 = ShortURL.objects.create(
            original_url="https://www.github.com",
            short_code="def456",
            clicks=10
        )
        
        self.test_url_3 = ShortURL.objects.create(
            original_url="https://stackoverflow.com",
            short_code="ghi789",
            clicks=0
        )
        self.shorten_url = reverse('api_shorten')
        self.redirect_url_base = '/api/<str:short_code>'
        self.stats_url_base = '/api/stats/<str:short_code>'
    
    def tearDown(self):
        ShortURL.objects.all().delete()