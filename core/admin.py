# core/admin.py
from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Service, Project, ServiceRequest, User

@admin.action(description='Выгрузить выбранные записи в XLSX')
def export_as_xlsx(modeladmin, request, queryset):
    model = modeladmin.model
    model_name = model._meta.model_name  # всегда строка
    verbose_name_plural = str(model._meta.verbose_name_plural)  # явно конвертируем в строку
    # Используем безопасный заголовок (макс. 31 символ для Excel)
    sheet_title = (verbose_name_plural[:30] if verbose_name_plural != 'service requests' else 'Заявки') or model_name
    # Заголовки полей
    field_names = [field.verbose_name or field.name for field in model._meta.fields]
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"{model_name}_export.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title  
    # Записываем заголовки
    ws.append(field_names)
    # Записываем данные
    for obj in queryset:
        row = []
        for field in model._meta.fields:
            value = getattr(obj, field.name)
            if value is None:
                row.append('')
            elif isinstance(value, bool):
                row.append('Да' if value else 'Нет')
            else:
                row.append(str(value))
        ws.append(row)

    wb.save(response)
    return response

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    actions = [export_as_xlsx]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'area', 'year')
    actions = [export_as_xlsx]

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'created_at')
    list_filter = ('status', 'service')
    actions = [export_as_xlsx]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    actions = [export_as_xlsx]