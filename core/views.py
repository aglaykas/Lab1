
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ServiceSerializer, ServiceRequestSerializer
from .models import Service, ServiceRequest, User
from django.http import HttpResponse
from openpyxl import Workbook
from collections import defaultdict

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {'username': user.username, 'role': user.role}
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def service_list(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service_request(request):
    if request.user.role == 'guest':
        return Response({'error': 'Гости не могут отправлять заявки'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ServiceRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_report(request):
    if request.user.role != 'admin':
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)
    table = request.GET.get('table')
    fields = request.GET.getlist('fields')  
    if not table or not fields:
        return Response({'error': 'Укажите таблицу и поля'}, status=status.HTTP_400_BAD_REQUEST)
    models_map = {
        'user': User,
        'service': Service,
        'servicerequest': ServiceRequest,
        'project': Project,
    }

    model = models_map.get(table.lower())
    if not model:
        return Response({'error': 'Недопустимая таблица'}, status=status.HTTP_400_BAD_REQUEST)

    valid_fields = [f.name for f in model._meta.fields]
    for f in fields:
        if f not in valid_fields:
            return Response({'error': f'Поле "{f}" не существует в таблице "{table}"'}, status=status.HTTP_400_BAD_REQUEST)

    queryset = model.objects.values(*fields)

    wb = Workbook()
    ws = wb.active
    ws.title = table.capitalize()
    ws.append(fields)
  
    for row in queryset:
        ws.append([str(row.get(f, '')) for f in fields])
   
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={table}_export.xlsx'
    wb.save(response)
    return response
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def contacts(request):
    return render(request, 'contacts.html')
    User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'role': request.user.role
    })

