from services import models
from django.contrib import admin


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')


@admin.register(models.Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'salary',
        'responsible_name',
        'responsible_phone',
        'end_date',
        # TODO. Add services num and employees num
    )
    search_fields = (
        'company_name',
        'responsible_name',
        'responsible_phone',
        'profile_requirements',
        'docs_requirements',
        'uniforms',
        'safety_equipment',
    )
    list_filter = ('effective_date', 'salary', 'start_date')
    
    # CUSTOM FIELDS
    def end_date(self, obj):
        """ Return the effective_date date in a specific format """
        return obj.effective_date.strftime("%d/%b/%Y")
    
    # Labels for custom fields
    end_date.short_description = 'Fecha de vigencia'
    end_date.admin_order_field = 'effective_date'
    

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'agreement',
        'schedule',
        'employee',
        'description',
        'location',
    )
    search_fields = (
        'agreement__company_name',
        'schedule__name',
        'employee__last_name_1',
        'employee__last_name_2',
        'description',
        'location',
    )
    list_filter = ('agreement', 'schedule', 'employee')