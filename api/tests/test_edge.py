from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from main.models import ShortURL
from .test_base import BaseAPITestCase
import json

class EdgeCasesTests(BaseAPITestCase):
    
    def test_extremely_long_url(self):
        long_url = "https://" + "a" * 1000 + ".com"
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': long_url}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_url_with_special_characters(self):
        url_with_specials = "https://example.com/path?param=value&list[]=1#fragment"
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': url_with_specials}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['original_url'], url_with_specials)
    
    def test_unicode_url(self):
        unicode_url = "https://пример.рф/путь"
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': unicode_url}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    

    def test_max_int_clicks(self):
        url = ShortURL.objects.create(
            original_url="https://max-clicks.com",
            short_code="max123",
            clicks=2147483646
        )
        
        redirect_url = reverse('api_redirect', args=[url.short_code])
        response = self.client.get(redirect_url)
        
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        updated_url = ShortURL.objects.get(short_code=url.short_code)
        
        self.assertEqual(updated_url.clicks, 2147483647)
    
    def test_empty_string_url(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': ''}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_whitespace_url(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': '   '}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_sql_injection_attempt(self):
        malicious_input = "'; DROP TABLE main_shorturl; --"
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': malicious_input}),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
        
        self.assertTrue(ShortURL.objects.exists())