from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from core.admin import export_as_xlsx
from core.models import Service

User = get_user_model()

class AdminExportTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='123'
        )
        self.service = Service.objects.create(name='Коттедж', description='...')

    