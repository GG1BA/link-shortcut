from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from main.models import ShortURL
from .test_base import BaseAPITestCase

class StatsEndpointTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.valid_short_code = self.test_url_1.short_code
        self.invalid_short_code = "nonexistent"
        self.stats_url = reverse('api_stats', args=[self.valid_short_code])
    
    def test_get_stats_success(self):
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.test_url_1.original_url)
        self.assertEqual(response.data['short_code'], self.valid_short_code)
        self.assertEqual(response.data['clicks'], self.test_url_1.clicks)
        self.assertIn('short_url', response.data)
        self.assertIn('created_at', response.data)
    
    def test_get_stats_invalid_code(self):
        url = reverse('api_stats', args=[self.invalid_short_code])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_stats_after_redirect(self):
        redirect_url = reverse('api_redirect', args=[self.valid_short_code])
        self.client.get(redirect_url)
        
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['clicks'], self.test_url_1.clicks + 1)
    
    def test_get_stats_empty_code(self):
        url = self.client.get('/api/')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_stats_wrong_method(self):
        response = self.client.post(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_stats_response_structure(self):
        response = self.client.get(self.stats_url)
        
        expected_fields = ['original_url', 'short_code', 'short_url', 'clicks', 'created_at']
        for field in expected_fields:
            self.assertIn(field, response.data)
        
        self.assertIsInstance(response.data['original_url'], str)
        self.assertIsInstance(response.data['short_code'], str)
        self.assertIsInstance(response.data['clicks'], int)