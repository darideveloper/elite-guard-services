from django.utils import timezone
from django.contrib import admin

from assistance import models

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
        if self.value() == 'today':
            return queryset.filter(date=timezone.now().date())
        elif self.value() == 'week':
            return queryset.filter(date__week=timezone.now().isocalendar()[1])
        elif self.value() == 'month':
            return queryset.filter(date__month=timezone.now().month)
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


# MODELS


@admin.register(models.Assistance)
class AssistanceAdmin(admin.ModelAdmin):
    """ Assistance model admin """
    list_display = (
        'date',
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
    )
    readonly_fields = (
        'service',
        'date',
        'weekly_assistance',
    )
    
    
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
    
    # Labels for custom fields
    company_name.short_description = 'Empresa'
    employee.short_description = 'Empleado'