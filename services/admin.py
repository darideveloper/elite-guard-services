from services import models
from django.contrib import admin


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "weekly_attendances", "hours", "start_time", "end_time")


@admin.register(models.Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "salary",
        "responsible_name",
        "responsible_phone",
        "effective_date",
    )
    search_fields = (
        "company_name",
        "responsible_name",
        "responsible_phone",
        "profile_requirements",
        "docs_requirements",
        "uniforms",
        "safety_equipment",
    )
    list_filter = ("effective_date", "salary", "start_date")


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "agreement",
        "schedule",
        "employee",
        "description",
        "location",
    )
    search_fields = (
        "agreement__company_name",
        "schedule__name",
        "employee__last_name_1",
        "employee__last_name_2",
        "description",
        "location",
    )
    list_filter = ("agreement", "schedule", "employee")
