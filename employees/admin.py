from django.contrib import admin
from employees import models


@admin.register(models.Colony)
class ColonyAdmin(admin.ModelAdmin):
    """ Colony model admin """
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
        'name',
        'last_name',
        'daily_rate',
        'status',
        'administrative_violations',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'name',
        'last_name',
        'curp',
        'rfc',
        'imss',
        'infonavit',
        'address',
        'phone',
        'anti_doping_results',
        'administrative_comments',
    )
    list_filter = (
        'status',
        'marital_status',
        'colony',
        'municipality',
        'bank',
        'daily_rate',
    )
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at', 'status_history', 'balance')
    

@admin.register(models.WeeklyLoan)
class WeeklyLoanAdmin(admin.ModelAdmin):
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

    