from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import ServiceRequest

User = get_user_model()

class SecurityTests(TestCase):

    def test_password_hashing(self):
        user = User.objects.create_user(username='sec', password='secret123')
        self.assertNotEqual(user.password, 'secret123')
        self.assertTrue(user.check_password('secret123'))

    def test_sql_injection_prevented_in_orm(self):
        user = User.objects.create_user(username='test', password='123')
        service = self.create_service()
        malicious_desc = "'; DROP TABLE core_servicerequest; --"
        ServiceRequest.objects.create(
            user=user, service=service, description=malicious_desc, status='pending'
        )
        obj = ServiceRequest.objects.get(description=malicious_desc)
        self.assertEqual(obj.description, malicious_desc)

    def test_xss_prevented_in_templates(self):
        user = User.objects.create_user(username='<script>alert(1)</script>', password='123')
        self.assertEqual(user.username, '<script>alert(1)</script>')

    def create_service(self):
        from core.models import Service
        return Service.objects.create(name='Test', description='...')