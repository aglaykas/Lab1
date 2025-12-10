from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Service, Project, ServiceRequest, TimeStampedModel
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class ModelTests(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='pass123', role='user')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('pass123'))
        self.assertEqual(user.role, 'user')

    def test_service_creation(self):
        service = Service.objects.create(name='Коттедж', description='...')
        self.assertEqual(service.name, 'Коттедж')
        self.assertIsNotNone(service.created_at)
        self.assertIsNotNone(service.updated_at)

    def test_project_service_foreign_key(self):
        service = Service.objects.create(name='Коттедж', description='...')
        project = Project.objects.create(
            title='Проект 1', description='...', service=service, area=200, year=2023
        )
        self.assertEqual(project.service, service)
        self.assertIn(project, service.projects.all())

    def test_service_request_creation(self):
        user = User.objects.create_user(username='client', password='123')
        service = Service.objects.create(name='Коттедж', description='...')
        request = ServiceRequest.objects.create(
            user=user, service=service, description='Хочу дом', status='pending'
        )
        self.assertEqual(request.user, user)
        self.assertEqual(request.service, service)

    def test_timestamped_fields_auto_set(self):
        service = Service.objects.create(name='Test', description='Desc')
        self.assertIsNotNone(service.created_at)
        self.assertIsNotNone(service.updated_at)