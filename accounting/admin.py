from django.contrib import admin

from accounting import models
from utils.admin_filters import (
    YearFilter, WeekNumberFilter
)


@admin.register(models.Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'skip_payment',
        'weekly_assistance',
        'employee',
        'work_days',
        'no_attendance_days',
        'sub_total',
    )
    list_filter = (
        'weekly_assistance__service',
        WeekNumberFilter,
        YearFilter,
        'employee',
        'skip_payment'
    )
    list_editable = (
        'skip_payment',
    )
    readonly_fields = (
        'sub_total',
    )
    ordering = (
        'id',
    )
    year_filter_field = "weekly_assistance__start_date"
    week_filter_field = "weekly_assistance__week_number"