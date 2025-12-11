
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contacts/', views.contacts, name='contacts'),
    path('auth/register/', views.register, name='register'),
    path('auth/user/', views.get_user_info, name='user_info'),
    path('requests/', views.create_service_request, name='create_request'),
]
