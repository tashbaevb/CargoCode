from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/api/map/', {'long': '11','short':'22'}, format='json')

