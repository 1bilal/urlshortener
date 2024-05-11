from django.test import TestCase

from .models import URL

class URLModelTestCase(TestCase):
    def test_create_url(self):
        # Create a new URL instance
        url = URL.objects.create(
            long_url='https://www.example.com/',
            short_url='abc123'
        )
        # Check that the URL was created successfully
        self.assertIsNotNone(url)
        self.assertEqual(url.long_url, 'https://www.example.com/')
        self.assertEqual(url.short_url, 'abc123')

    def test_query_url(self):
        # Create a new URL instance
        URL.objects.create(
            long_url='https://www.example.com/',
            short_url='abc123'
        )
        # Query the database for the URL
        url = URL.objects.get(short_url='abc123')
        # Check that the URL was retrieved successfully
        self.assertIsNotNone(url)
        self.assertEqual(url.long_url, 'https://www.example.com/')
