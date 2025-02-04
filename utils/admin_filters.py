from django.contrib import admin
from django.utils import timezone

from utils.dates import get_current_week


class TodayDateFilter(admin.SimpleListFilter):
    """ Custom detae filter with default value: today """
    title = 'Fecha'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Hoy'),
            ('all', 'Todas las fechas (filtrar por año y semana)'),
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
                date__week=timezone.now().astimezone(
                    time_zone).isocalendar()[1]
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
        
        # Get field name
        field_name = getattr(model_admin, "week_filter_field", "week_number")
        WeekNumberFilter.field_name = field_name
        
        # Get all distinct week numbers from the dataset
        week_numbers = model_admin.get_queryset(
            request).values(WeekNumberFilter.field_name).distinct()
        current_week = get_current_week()

        # Generate the options
        options = []
        for week_number in week_numbers:
            if week_number[WeekNumberFilter.field_name] == current_week:
                options.append((
                    week_number[WeekNumberFilter.field_name],
                    f'Semana actual ({current_week})'
                ))
            else:
                options.append((
                    week_number[WeekNumberFilter.field_name],
                    f'Semana {week_number[WeekNumberFilter.field_name]}'
                ))

        return options

    def queryset(self, request, queryset):
        """ Filters the queryset based on the selected value """
        if self.value():
            return queryset.filter(**{WeekNumberFilter.field_name: self.value()})
        return queryset

    def value(self):
        """ Sets the default value to the current week number """
        value = super().value()
        if value is None:
            return str(get_current_week())
        return value


class YearFilter(admin.SimpleListFilter):
    title = "Año"
    parameter_name = "year"
    field_name = ""

    def lookups(self, request, model_admin):
        """ Defines the available options in the filter """
        
        # Get field name
        field_name = getattr(model_admin, "year_filter_field", "start_date")
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