from django.contrib import admin
from django.utils.html import format_html

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
        'created_at',
        'name',
        'last_name_1',
        'last_name_2',
        'daily_rate',
        'birthdate',
        'neighborhood',
        'address_street',
        'address_number',
        'acciones',
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

    def acciones(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Imprimir</a>'
            '<br />'
            '<a class="button" href="{}" target="_blank">Ver</a>',
            f"/employees/report/employee-details/{obj.id}",
            f"/employees/report/employee-preview/{obj.id}",
        )
    

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
    