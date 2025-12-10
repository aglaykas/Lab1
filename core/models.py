# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Гость'),
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_set',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)

class Service(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    area = models.FloatField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class ServiceRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
        ('rejected', 'Отклонено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} — {self.service.name}"