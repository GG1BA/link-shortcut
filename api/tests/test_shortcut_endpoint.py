from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from main.models import ShortURL
from .test_base import BaseAPITestCase
import json

class ShortenEndpointTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.valid_payload = {
            'original_url': 'https://www.example.com/very/long/url'
        }
        self.invalid_payload = {
            'original_url': 'not-a-valid-url'
        }
    
    def test_create_short_url_success(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_code', response.data)
        self.assertIn('original_url', response.data)
        self.assertIn('short_url', response.data)
        self.assertEqual(response.data['original_url'], self.valid_payload['original_url'])
        self.assertEqual(response.data['clicks'], 0)
        
        short_code = response.data['short_code']
        self.assertTrue(ShortURL.objects.filter(short_code=short_code).exists())
    
    def test_create_short_url_without_protocol(self):
        payload = {'original_url': 'example.com'}
        response = self.client.post(
            self.shorten_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['original_url'].startswith('https://'))
    
    def test_create_short_url_invalid_url(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('original_url', response.data)
    
    def test_create_short_url_empty_payload(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_short_url_missing_field(self):
        response = self.client.post(
            self.shorten_url,
            data=json.dumps({'wrong_field': 'value'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_duplicate_url(self):
        response1 = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': 'https://duplicate.com'}),
            content_type='application/json'
        )
        response2 = self.client.post(
            self.shorten_url,
            data=json.dumps({'original_url': 'https://duplicate.com'}),
            content_type='application/json'
        )
        
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response1.data['short_code'], response2.data['short_code'])
    
    def test_create_short_url_wrong_method(self):
        response = self.client.get(self.shorten_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_create_short_url_malformed_json(self):
        response = self.client.post(
            self.shorten_url,
            data='{"malformed json"',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)