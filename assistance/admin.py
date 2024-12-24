from django.utils import timezone
from django.contrib import admin

from assistance import models


class TodayDateFilter(admin.SimpleListFilter):
    title = 'Fecha'  # Label for the filter
    parameter_name = 'date'  # Query parameter in the URL

    def lookups(self, request, model_admin):
        return [
            ('today', 'Hoy'),
            ('week', 'Esta semana'),
            ('month', 'Este mes'),
            ('all', 'Todas las fechas'),
        ]

    def queryset(self, request, queryset):
        # Filter by today if the 'today' option is selected
        if self.value() == 'today':
            return queryset.filter(date=timezone.now().date())
        elif self.value() == 'week':
            return queryset.filter(date__week=timezone.now().isocalendar()[1])
        elif self.value() == 'month':
            return queryset.filter(date__month=timezone.now().month)
        return queryset

    def value(self):
        # Set default to 'today' if no filter is applied
        value = super().value()
        return value or 'today'  # Default to 'today'


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