from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html

from assistance import models
from utils.dates import get_week_day


# FILTERS


class TodayDateFilter(admin.SimpleListFilter):
    """ Custom detae filter with default value: today """
    title = 'Fecha'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Hoy'),
            ('week', 'Esta semana'),
            ('month', 'Este mes'),
            ('all', 'Todas las fechas'),
        ]

    def queryset(self, request, queryset):
        # Value is the selected filter
        time_zone = timezone.get_current_timezone()
        if self.value() == 'today':
            return queryset.filter(
                date=timezone.now().astimezone(time_zone).date()
            )
        elif self.value() == 'week':
            return queryset.filter(
                date__week=timezone.now().astimezone(time_zone).isocalendar()[1]
            )
        elif self.value() == 'month':
            return queryset.filter(
                date__month=timezone.now().astimezone(time_zone).month
            )
        return queryset

    def value(self):
        # Set default to 'today'
        value = super().value()
        return value or 'today'
    
    
class WeekNumberFilter(admin.SimpleListFilter):
    """ Custom filter for week number with default value as the current week """
    title = 'Número de Semana'
    parameter_name = 'week_number'

    def lookups(self, request, model_admin):
        """ Defines the available options in the filter """
        # Get all distinct week numbers from the dataset
        week_numbers = model_admin.get_queryset(request).values('week_number').distinct()
        current_week = timezone.now().isocalendar()[1]
        options = []
        
        # Generate the options
        for week_number in week_numbers:
            if week_number['week_number'] == current_week:
                options.append((
                    week_number['week_number'],
                    f'Semana actual ({current_week})'
                ))
            else:
                options.append((
                    week_number['week_number'],
                    f'Semana {week_number["week_number"]}'
                ))

        return options

    def queryset(self, request, queryset):
        """ Filters the queryset based on the selected value """
        if self.value():
            return queryset.filter(week_number=self.value())
        return queryset

    def value(self):
        """ Sets the default value to the current week number """
        value = super().value()
        if value is None:
            return str(timezone.now().isocalendar()[1])
        return value


class YearFilter(admin.SimpleListFilter):
    """ Custom filter for year with default value as the current year """
    title = "Año"
    parameter_name = "year"
    
    def lookups(self, request, model_admin):
        """ Defines the available options in the filter """
        
        years = model_admin.get_queryset(request).values(
            'start_date__year'
        ).distinct()
        options = [
            (year['start_date__year'], year['start_date__year'])
            for year in years
        ]
        return options
    
    def queryset(self, request, queryset):
        """ Filters the queryset based on the selected value """
        if self.value():
            return queryset.filter(start_date__year=self.value())
        return queryset
    
    def value(self):
        """ Sets the default value to the current year """
        value = super().value()
        if value is None:
            return str(timezone.now().year)
        return value
        
        
# MODELS


@admin.register(models.Assistance)
class AssistanceAdmin(admin.ModelAdmin):
    """ Assistance model admin """
    list_display = (
        'date',
        'week_day_name',
        'service',
        'attendance',
        'extra_paid_hours',
        'extra_unpaid_hours',
        'notes',
    )
    search_fields = (
        'service__agreement__company_name',
        'service__location',
        'service__description',
        'service__employee__name',
        'service__employee__last_name_1',
        'service__employee__last_name_2',
        'notes',
    )
    list_filter = (
        TodayDateFilter,
        'service__agreement__company_name',
        'service__employee',
        'attendance',
        'weekly_assistance__week_number',
    )
    readonly_fields = (
        'service',
        'date',
        'weekly_assistance',
    )
    
    # Custom fields
    
    def week_day_name(self, obj):
        """ Return the name of the week day """
        return get_week_day(obj.date)
            
    # Labels for custom fields
    week_day_name.short_description = 'Día de la semana'
    
    
@admin.register(models.WeeklyAssistance)
class WeeklyAssistanceAdmin(admin.ModelAdmin):
    """ Weekly assistance model admin """
    
    list_display = (
        'company_name',
        'employee',
        'week_number',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
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
        'service__agreement__company_name',
        'service__employee',
        WeekNumberFilter,
        YearFilter,
        'start_date',
        'end_date',
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
    )
    
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
        
        return format_html(
            '<a class="btn btn-primary my-1 w-110" href="{}">Editar Dias</a>',
            "/admin/assistance/assistance/?"
            f"service__employee__id__exact={employee_id}"
            f"&weekly_assistance__week_number={week_number}"
        )
    
    # Labels for custom fields
    company_name.short_description = 'Empresa'
    employee.short_description = 'Empleado'
    custom_links.short_description = 'Acciones'