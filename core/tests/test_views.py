from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Service, ServiceRequest
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class ViewTests(TestCase):

    def test_homepage_status(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_services_page_status(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)

