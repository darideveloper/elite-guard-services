
from django.urls import path
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render

from employees import models


@admin.register(models.Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    """ Neighborhood model admin """
    list_display = ('name',)
    
    
@admin.register(models.Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    """ Municipality model admin """
    list_display = ('name',)
    
    
@admin.register(models.MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    """ MaritalStatus model admin """
    list_display = ('name',)
    
    
@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """ Status model admin """
    list_display = ('name',)
    
    
@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    """ Bank model admin """
    list_display = ('name',)
     
    
@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """ Employee model admin """
    list_display = (
        'start_date',
        'name',
        'last_name_1',
        'last_name_2',
        'daily_rate',
        'birthdate',
        'neighborhood',
        'address_street',
        'address_number',
        'custom_links',
    )
    search_fields = (
        'name',
        'last_name_1',
        'curp',
        'rfc',
        'imss',
        'infonavit',
        'ine',
        'phone',
        'anti_doping_results',
        'administrative_comments',
    )
    list_filter = (
        'marital_status',
        'education',
        'municipality_birth',
        'status',
        'municipality',
        'neighborhood',
        'bank',
        'created_at',
        'updated_at',
    )
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at', 'status_history', 'balance')
    fieldsets = (
        (
            "General", {
                'fields': (
                    'name',
                    'last_name_1',
                    'last_name_2',
                    'height',
                    'weight',
                    'marital_status',
                    'education',
                    'languages',
                    'photo',
                ),
            }
        ),
        (
            "Nacimiento", {
                'fields': (
                    'birthdate',
                    'municipality_birth'
                ),
            }
        ),
        (
            "Laboral", {
                'fields': (
                    'daily_rate',
                    'curp',
                    'rfc',
                    'imss',
                    'infonavit',
                    'ine',
                    'uniform_date',
                    'status',
                    'status_change_details',
                    'knowledge',
                    'skills',
                ),
            }
        ),
        (
            "Contacto", {
                'fields': (
                    'municipality',
                    'neighborhood',
                    'postal_code',
                    'address_street',
                    'address_number',
                    'phone',
                    'emergency_phone',
                ),
            }
        ),
        (
            "Banco", {
                'fields': (
                    'bank',
                    'card_number',
                    'balance',
                ),
            }
        ),
        (
            "Otro", {
                'fields': (
                    'anti_doping_results',
                    'administrative_violations',
                    'administrative_comments',
                    'status_history',
                    'created_at',
                    'updated_at',
                ),
            }
        ),
    )

    # Custom list fields
    def custom_links(self, obj):
        return format_html(
            '<a class="btn btn-primary my-1" href="{}" target="_blank">Imprimir</a>'
            '<br />'
            '<a class="btn btn-primary my-1" href="{}">Ver</a>',
            f"/employees/report/employee-details/{obj.id}",
            f"/admin/employees/employee/{obj.id}/preview/",
        )
    
    def start_date(self, obj):
        return obj.created_at.strftime("%d/%b/%Y")
    
    # Labels for custom fields
    custom_links.short_description = 'Acciones'
    start_date.short_description = 'Fecha de alta'
    start_date.admin_order_field = 'created_at'
    
    def get_urls(self):
        # Setup urls
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/preview/',
                self.admin_site.admin_view(self.employee_preview),
                name='employee_preview',
            ),
        ]
        return custom_urls + urls
    
    def employee_preview(self, request, pk):
        # Custom view to render employee preview
        
        # Get employee
        employee = models.Employee.objects.get(pk=pk)
        
        # Add specific employee data to the context
        last_name = employee.last_name_1
        if employee.last_name_2:
            last_name += " " + employee.last_name_2
        uniform_date = "N/A"
        if employee.uniform_date:
            uniform_date = employee.uniform_date.strftime("%d/%m/%Y")
        
        # Get admin context
        context = self.admin_site.each_context(request)
        context['employee_data'] = {
            "Nombre": employee.name.title(),
            "Apellidos": last_name.title(),
            "Servicio": employee.service,
            "Sueldo": f"$ {employee.daily_rate} / dia",
            "Fecha de nacimiento": employee.birthdate.strftime("%d/%m/%Y"),
            "Edad": employee.get_age(),
            "RFC": employee.rfc if employee.rfc else "N/A",
            "CURP": employee.curp if employee.curp else "N/A",
            "IMSS": employee.imss if employee.imss else "N/A",
            "Infonavit": employee.infonavit if employee.infonavit else "N/A",
            "Estado Civil": employee.marital_status.name,
            "Dirección": f"{employee.address_street} {employee.address_number}".title(),
            "Colonia": employee.neighborhood.name,
            "Municipio": employee.municipality.name,
            "C.P.": employee.postal_code,
            "Teléfono": employee.phone,
            "Banco": employee.bank.name if employee.bank else "N/A",
            "Numero de tarjeta": employee.card_number if employee.card_number else "N/A",
            "Fecha de uniforme": uniform_date,
            "Activo": "Si" if employee.status.name == "Activo" else "No",
        }
        full_name = f"{employee.name.title()} {last_name.title()}"
        context['title'] = f"Vista previa de {full_name}"
        
        # Render preview
        return render(request, 'employees/reports/employee-preview.html', context)
    

@admin.register(models.Loan)
class Loan(admin.ModelAdmin):
    """ WeklyLoan model admin """
    list_display = (
        'employee',
        'amount',
        'date',
    )
    search_fields = (
        'employee__name',
        'employee__last_name',
        'employee__rfc',
        'employee__curp',
    )
    list_filter = (
        'employee',
        'date',
    )
    list_per_page = 20


@admin.register(models.Ref)
class RefAdmin(admin.ModelAdmin):
    """ Ref model admin """
    list_display = (
        'employee',
        'name',
        'phone',
    )
    search_fields = (
        'employee__name',
        'employee__last_name',
        'employee__rfc',
        'employee__curp',
    )
    list_filter = (
        'employee',
    )
    list_per_page = 20
    
    
@admin.register(models.Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    """ Relationship model admin """
    list_display = ('name',)
    

@admin.register(models.Relative)
class RelativeAdmin(admin.ModelAdmin):
    """ Relative model admin """
    list_display = (
        'employee',
        'name',
        'last_name_1',
        'last_name_2',
        'relationship',
    )
    search_fields = (
        'employee__name',
        'employee__last_name',
        'employee__rfc',
        'employee__curp',
    )
    list_filter = (
        'employee',
        'relationship',
    )
    list_per_page = 20
    