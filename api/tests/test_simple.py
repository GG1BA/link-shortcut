from django.test import TestCase
from rest_framework.test import APIClient
from main.models import ShortURL

class SimpleTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.test_url = ShortURL.objects.create(
            original_url="https://test.com",
            short_code="test123",
            clicks=0
        )
    
    def test_model_creation(self):
        self.assertEqual(self.test_url.original_url, "https://test.com")
        self.assertEqual(self.test_url.short_code, "test123")
        self.assertEqual(self.test_url.clicks, 0)
    
    def test_increment_clicks(self):
        self.test_url.increment_clicks()
        self.assertEqual(self.test_url.clicks, 1)
    
    def test_api_client_works(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 301, 302, 404])