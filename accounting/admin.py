from django.contrib import admin
from django.utils.html import format_html

from accounting import models
from utils.admin_filters import (
    YearFilter, WeekNumberFilter
)
from utils.excel import get_excel_response


@admin.register(models.Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'agreement_name',
        'employee_name',
        'skip_payment',
        'weekly_rate',
        'daily_rate',
        'thursday_assistance',
        'friday_assistance',
        'saturday_assistance',
        'sunday_assistance',
        'monday_assistance',
        'tuesday_assistance',
        'wednesday_assistance',
        'worked_days',
        'no_attendance_days',
        'no_attendance_penalty',
        'penalties_amount',
        'bonuses_amount',
        'other_amount',
        'extra_unpaid_hours_amount',
        'subtotal',
        'discount_amount',
        'discount_loans',
        'location',
        'bank',
        'card_number',
        'total',
        'paid',
    )
    list_filter = (
        'weekly_assistance__service',
        WeekNumberFilter,
        YearFilter,
        'skip_payment'
    )
    list_editable = (
        'skip_payment',
        'paid',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    ordering = (
        'id',
    )
    readonly_fields = (
        'discount_loans',
    )
    year_filter_field = "weekly_assistance__start_date"
    week_filter_field = "weekly_assistance__week_number"
    
    # reusable methods
    def __get_boolean_icon__(self, value: bool):
        """ Return a boolean icon
        
        Args:
            value (bool): The boolean value to evaluate
        """
        if value:
            image = "icon-yes.svg"
        else:
            image = "icon-no.svg"
            
        return format_html(
            '<img src="/static/admin/img/{}" alt="False">',
            image
        )
    
    # Custom fields
    def thursday_assistance(self, obj):
        """ Return the assistance of the thursday """
        return self.__get_boolean_icon__(obj.get_day_assistance("thursday"))
    
    def friday_assistance(self, obj):
        """ Return the assistance of the friday """
        return self.__get_boolean_icon__(obj.get_day_assistance("friday"))
    
    def saturday_assistance(self, obj):
        """ Return the assistance of the saturday """
        return self.__get_boolean_icon__(obj.get_day_assistance("saturday"))
    
    def sunday_assistance(self, obj):
        """ Return the assistance of the sunday """
        return self.__get_boolean_icon__(obj.get_day_assistance("sunday"))
    
    def monday_assistance(self, obj):
        """ Return the assistance of the monday """
        return self.__get_boolean_icon__(obj.get_day_assistance("monday"))
    
    def tuesday_assistance(self, obj):
        """ Return the assistance of the tuesday """
        return self.__get_boolean_icon__(obj.get_day_assistance("tuesday"))
    
    def wednesday_assistance(self, obj):
        """ Return the assistance of the wednesday """
        return self.__get_boolean_icon__(obj.get_day_assistance("wednesday"))
    
    # Labels for custom fields
    thursday_assistance.short_description = 'J'
    friday_assistance.short_description = 'V'
    saturday_assistance.short_description = 'S'
    sunday_assistance.short_description = 'D'
    monday_assistance.short_description = 'L'
    tuesday_assistance.short_description = 'M'
    wednesday_assistance.short_description = 'X'
    
    # Custom actions
    def export_excel(self, request, queryset):
        """ Export the selected payrolls to an excel file with custom styles """
        
        return get_excel_response(queryset, "Nómina Semana")
    
    export_excel.short_description = 'Exportar a Excel'
    actions = [export_excel]
    
    
@admin.register(models.PayrollSummary)
class PayrollSummaryAdmin(admin.ModelAdmin):
    list_display = (
        'agreement_name',
        'employee_name',
        'skip_payment',
        'bank',
        'card_number',
        'total',
        'paid',
    )
    list_filter = (
        'weekly_assistance__service',
        WeekNumberFilter,
        YearFilter,
        'skip_payment'
    )
    list_editable = (
        'skip_payment',
        'paid',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    ordering = (
        'id',
    )
    year_filter_field = "weekly_assistance__start_date"
    week_filter_field = "weekly_assistance__week_number"