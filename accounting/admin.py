from django.contrib import admin
from django.utils import timezone

from accounting import models


# FILTERS

class YearFilter(admin.SimpleListFilter):
    title = "Año"
    parameter_name = "year"
    field_name = ""

    def lookups(self, request, model_admin):
        """ Defines the available options in the filter """
        field_name = getattr(
            model_admin,
            "year_filter_field",
            "weekly_assistance__start_date"
        )
        YearFilter.field_name = field_name
        years = model_admin.get_queryset(request).values(
            f"{YearFilter.field_name}__year"
        ).distinct()
        years_values = [year[f"{YearFilter.field_name}__year"]
                        for year in years]
        years_unique = list(set(years_values))
        options = []
        for year in years_unique:
            options.append((str(year), year))
        return options

    def queryset(self, request, queryset):
        """ Filters the queryset based on the selected value """
        if self.value():
            return queryset.filter(**{f"{YearFilter.field_name}__year": self.value()})
        return queryset

    def value(self):
        """ Sets the default value to the current year """
        value = super().value()
        if value is None:
            return str(timezone.now().year)
        return value


# MODELS

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
        'weekly_assistance__week_number',
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
#     save_on_top = True
#     save_as = True
#     actions_on_top = True
#     actions_on_bottom = False
#     actions_selection_counter = True
#     date_hierarchy = 'created_at'
#     empty_value_display = '-empty-'
#     show_full_result_count = True
#     show_all = True
#     show_change_link = True
#     show_delete_link = True
#     show_save_and_add_another = True
#     show_save_and_continue = True
#     show_save = True
#     show_history = True
#     show_add = True
#     show_changelist = True
