from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class AuthTests(TestCase):


    def test_admin_can_access_admin_panel(self):
        admin = User.objects.create_superuser(username='admin', password='123')
        self.client.login(username='admin', password='123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def get_service(self):
        from core.models import Service
        return Service.objects.create(name='Test', description='...')

    def test_password_is_hashed(self):
        user = User.objects.create_user(username='test', password='mypassword')
        self.assertNotEqual(user.password, 'mypassword')
        self.assertTrue(user.check_password('mypassword'))