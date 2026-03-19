from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from main.models import ShortURL
from .test_base import BaseAPITestCase

class RedirectEndpointTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.valid_short_code = self.test_url_1.short_code
        self.invalid_short_code = "nonexistent"
        self.redirect_url = reverse('api_redirect', args=[self.valid_short_code])
    
    def test_redirect_success(self):
        url = reverse('api_redirect', args=[self.valid_short_code])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.data['original_url'], self.test_url_1.original_url)
        updated_url = ShortURL.objects.get(short_code=self.valid_short_code)
        self.assertEqual(updated_url.clicks, self.test_url_1.clicks + 1)
    
    def test_redirect_invalid_code(self):
        url = reverse('api_redirect', args=[self.invalid_short_code])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_redirect_multiple_times(self):
        url = reverse('api_redirect', args=[self.valid_short_code])
        
        for i in range(5):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        updated_url = ShortURL.objects.get(short_code=self.valid_short_code)
        self.assertEqual(updated_url.clicks, self.test_url_1.clicks + 5)
    
    def test_redirect_empty_code(self):
        url = self.client.get('/api/')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_redirect_with_zero_clicks(self):
        url = reverse('api_redirect', args=[self.test_url_3.short_code])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('Location', response.headers)
        self.assertEqual(response.headers['Location'], self.test_url_3.original_url)
        
        updated_url = ShortURL.objects.get(short_code=self.test_url_3.short_code)
        self.assertEqual(updated_url.clicks, 1)
    
    def test_redirect_wrong_method(self):
        url = reverse('api_redirect', args=[self.valid_short_code])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)