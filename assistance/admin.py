from django.contrib import admin
from django.utils.html import format_html

from assistance import models
from utils.admin_filters import (
    TodayDateFilter, YearFilter, WeekNumberFilter
)
from utils.excel import get_excel_response


@admin.register(models.Assistance)
class AssistanceAdmin(admin.ModelAdmin):
    """ Assistance model admin """
    list_display = (
        'employee',
        'company',
        'attendance',
        'extra_paid_hours',
        'extra_unpaid_hours',
        'custom_links',
        'notes',
    )
    search_fields = (
        'weekly_assistance__service__agreement__company_name',
        'weekly_assistance__service__location',
        'weekly_assistance__service__description',
        'weekly_assistance__service__employee__name',
        'weekly_assistance__service__employee__last_name_1',
        'weekly_assistance__service__employee__last_name_2',
        'notes',
    )
    list_filter = (
        YearFilter,
        'weekly_assistance__week_number',
        TodayDateFilter,
        'weekly_assistance__service__agreement__company_name',
        'weekly_assistance__service__employee',
        'attendance',
    )
    readonly_fields = (
        'date',
        'weekly_assistance',
    )
    year_filter_field = "date"
    ordering = ('-date',)
    list_editable = ('attendance', 'extra_paid_hours',
                     'extra_unpaid_hours', 'notes')

    # Custom fields
    def company(self, obj):
        """ Return the company name """
        return obj.weekly_assistance.service.agreement.company_name

    def employee(self, obj):
        """ Return the employee name """
        return str(obj.weekly_assistance.service.employee)
    
    def custom_links(self, obj):
        """ Create custom Imprimir and Ver buttons """

        # Generate links
        link_view = "/admin/assistance/extrapayment/?"
        link_view += f"assistance__id__exact={obj.id}"
        
        link_add = "/admin/assistance/extrapayment/add/?"
        link_add += f"assistance={obj.id}"

        return format_html(
            '<a class="btn btn-primary my-1 w-120" href="{}">Ver extras</a>'
            '<a class="btn btn-primary my-1 w-120" href="{}">Añadir extra</a>',
            link_view, link_add
        )

    # Labels for custom fields
    company.short_description = 'Empresa'
    employee.short_description = 'Empleado'
    custom_links.short_description = 'Acciones'


@admin.register(models.WeeklyAssistance)
class WeeklyAssistanceAdmin(admin.ModelAdmin):
    """ Weekly assistance model admin """

    list_display = (
        'company_name',
        'employee',
        'week_number',
        'thursday',
        'friday',
        'saturday',
        'sunday',
        'monday',
        'tuesday',
        'wednesday',
        'total_extra_paid_hours',
        'total_extra_unpaid_hours',
        'custom_links',
    )
    search_fields = (
        'service__agreement__company_name',
        'service__location',
        'service__description',
        'service__employee__name',
        'service__employee__last_name_1',
        'service__employee__last_name_2',
    )
    list_filter = (
        YearFilter,
        WeekNumberFilter,
        'service__agreement__company_name',
        'service__employee',
    )
    readonly_fields = (
        'service',
        'week_number',
        'start_date',
        'end_date',
        'total_extra_paid_hours',
        'total_extra_unpaid_hours',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
        'notes',
    )
    year_filter_field = "start_date"

    # Custom fields
    def company_name(self, obj):
        """ Return the company name """
        return obj.service.agreement.company_name

    def employee(self, obj):
        """ Return the employee name """
        return str(obj.service.employee)

    def custom_links(self, obj):
        """ Create custom Imprimir and Ver buttons """

        employee_id = obj.service.employee.id
        week_number = obj.week_number

        link = "/admin/assistance/assistance/?"
        link += f"weekly_assistance__service__employee__id__exact={
            employee_id}"
        link += f"&weekly_assistance__week_number={week_number}"
        link += f"&year={obj.start_date.year}"
        link += "&date=all"
        return format_html(
            '<a class="btn btn-primary my-1 w-110" href="{}">Editar Dias</a>',
            link
        )

    # Labels for custom fields
    company_name.short_description = 'Empresa'
    employee.short_description = 'Empleado'
    custom_links.short_description = 'Acciones'

    # Custom actions
    def export_excel(self, request, queryset):
        """ Export the queryset to an Excel file with custom styles """
        
        return get_excel_response(queryset, "Asistencias Semana")

    export_excel.short_description = 'Exportar a Excel'
    actions = [export_excel]


@admin.register(models.ExtraPaymentCategory)
class ExtraPaymentCategoryAdmin(admin.ModelAdmin):
    """ Extra payment category model admin """
    list_display = (
        'name',
        'description',
    )
    

@admin.register(models.ExtraPayment)
class ExtraPaymentAdmin(admin.ModelAdmin):
    """ Extra payment model admin """
    list_display = (
        'assistance',
        'category',
        'amount',
        'notes',
    )
    search_fields = (
        'notes',
    )
    list_filter = (
        'category',
        'assistance',
        'assistance__weekly_assistance__week_number',
        'assistance__weekly_assistance__service__agreement__company_name',
        'assistance__weekly_assistance__service__employee',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    raw_id_fields = ('assistance',)