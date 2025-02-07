from django.db import models
from django.conf import settings

from assistance import models as assistance_models


class Payroll(models.Model):
    id = models.AutoField(primary_key=True)
    skip_payment = models.BooleanField(
        default=False,
        verbose_name='Omitir pago'
    )
    weekly_assistance = models.ForeignKey(
        assistance_models.WeeklyAssistance,
        on_delete=models.CASCADE,
        verbose_name='Asistencia semanal'
    )
    discount_loans = models.FloatField(
        default=0,
        verbose_name='Descuento por préstamos',
    )
    created_at = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Fecha de actualización',
        auto_now=True,
    )
    
    class Meta:
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nóminas'
        
    def __str__(self):
        skip_value = "Sí" if self.skip_payment else "No"
        return f'{self.weekly_assistance} (Omitir: {skip_value})'
    
    # reusable methods
    def __get_extras__(self, category_name: str) -> assistance_models.ExtraPayment:
        """ Return the extra payments of the employee
        
        Args:
            category_name (str): Category name of the extra payment
        
        Returns:
            QuerySet: Extra payments of the employee
        """
        assistances = assistance_models.Assistance.objects.filter(
            weekly_assistance=self.weekly_assistance
        )
        extras_category = assistance_models.ExtraPaymentCategory.objects.get(
            name=category_name
        )
        extras = assistance_models.ExtraPayment.objects.filter(
            assistance__in=assistances,
            category=extras_category
        )
        return extras
    
    def __get_extras_amount__(self, category_name: str) -> float:
        """ Return the total amount of the extra payments
        
        Args:
            category_name (str): Category name of the extra payment
        
        Returns:
            float: Total amount of the extra payments
        """
        extras = self.__get_extras__(category_name)
        if not extras:
            total = 0
        total = sum([extra.amount for extra in extras])
        return total
    
    # Custom methods
    def get_day_assistance(self, day: str) -> bool:
        """ get the assistance of the employee in a specific day

        Args:
            day (str): Day of the week (e.g. 'monday')

        Returns:
            bool: True if the employee attended, False otherwise
        """
        return self.weekly_assistance.get_day_assistance(day)
    
    def get_hour_rate(self) -> float:
        """ get the hourly rate of the employee
        
        Returns:
            float: Hourly rate of the employee
        """
        hours = self.weekly_assistance.service.schedule.hours
        hour_rate = self.daily_rate / hours
        print("hours", hours)
        print("daily_rate", self.daily_rate)
        print("hour_rate", hour_rate)
        return hour_rate
    
    def get_data_header(self) -> list:
        """ get the header of the payroll data
        
        Returns:
            list: Header of the payroll data
        """
        
        return [
            'Servicio',
            'Empleado',
            'Omitir pago',
            'Salario semanal',
            'Salario diario',
            'j',
            'v',
            's',
            'd',
            'l',
            'm',
            'x',
            'Días trabajados',
            'Faltas',
            'Penalización por faltas',
            'Otras penalizaciones',
            'Bonos',
            'Otros',
            'Horas extras',
            'Subtotal',
            'Descuentos por robo o daño',
            'Descuento por préstamos',
            'Ubicación',
            'Banco',
            'Número de tarjeta',
            'A pagar',
        ]
        
    def get_data_list(self) -> list:
        """ get the data of the payroll
        
        Returns:
            list: Data of the payroll
        """
        
        return [
            self.agreement_name,
            self.employee_name,
            "sí" if self.skip_payment else "no",
            self.weekly_rate,
            self.daily_rate,
            'a' if self.get_day_assistance('thursday') else 'f',
            'a' if self.get_day_assistance('friday') else 'f',
            'a' if self.get_day_assistance('saturday') else 'f',
            'a' if self.get_day_assistance('sunday') else 'f',
            'a' if self.get_day_assistance('monday') else 'f',
            'a' if self.get_day_assistance('tuesday') else 'f',
            'a' if self.get_day_assistance('wednesday') else 'f',
            self.worked_days,
            self.no_attendance_days,
            self.no_attendance_penalty,
            self.penalties_amount,
            self.bonuses_amount,
            self.other_amount,
            self.extra_unpaid_hours_amount,
            self.subtotal,
            self.discount_amount,
            self.discount_loans,
            self.location,
            self.bank,
            self.card_number,
            self.total,
        ]
        
    def get_is_highlighted(self) -> bool:
        """ get if the payroll is highlighted
        
        Returns:
            bool: True if the payroll is highlighted, False otherwise
        """
        return self.skip_payment
    
    # Custom properties
    @property
    def agreement_name(self) -> str:
        """ get company name of the service agreement
        
        Returns:
            str: Company name of the service agreement
        """
        return self.weekly_assistance.service.agreement.company_name
    
    @property
    def employee_name(self) -> str:
        """ get employee full name
        
        Returns:
            str: Employee full name
        """
        return self.weekly_assistance.service.employee.get_full_name()
    
    @property
    def weekly_rate(self) -> float:
        """ get weekly rate of the employee

        Returns:
            float: Weekly rate of the employee
        """
        return self.weekly_assistance.service.employee.weekly_rate
    
    @property
    def daily_rate(self) -> float:
        """ get daily rate of the employee (based in the weekly rate and work days)

        Returns:
            float: Daily rate of the employee
        """
        work_days = self.weekly_assistance.service.schedule.weekly_attendances
        weekly_rate = self.weekly_assistance.service.employee.weekly_rate
        return int(weekly_rate / work_days * 100) / 100
    
    @property
    def worked_days(self) -> int:
        """ get the total of worked days
        
        Returns:
            int: Total of worked days
        """
        return self.weekly_assistance.get_worked_days()
    
    @property
    def no_attendance_days(self) -> int:
        """ get the total of days without attendance
        
        Returns:
            int: Total of days without attendance
        """
        return self.weekly_assistance.get_no_attendance_days()
    
    @property
    def no_attendance_penalty(self) -> float:
        """ get the total amount of the no attendance penalty
        
        Returns:
            float: Total amount of the no attendance penalty
        """
        return - self.no_attendance_days * settings.PENALTY_NO_ATTENDANCE
    
    @property
    def penalties_amount(self) -> float:
        """ get the total amount of the penalties
        
        Returns:
            float: Total amount of the penalties
        """
        return - self.__get_extras_amount__('Penalización')
    
    @property
    def bonuses_amount(self) -> float:
        """ get the total amount of the bonuses
        
        Returns:
            float: Total amount of the bonuses
        """
        return self.__get_extras_amount__('Bono')
    
    @property
    def other_amount(self) -> float:
        """ get the total amount of the other extras
        
        Returns:
            float: Total amount of the other extras
        """
        return self.__get_extras_amount__('Otro')
    
    @property
    def extra_unpaid_hours_amount(self) -> float:
        """ get the total amount of the extra hours
        
        Returns:
            float: Total amount of the extra hours
        """
        assistances = assistance_models.Assistance.objects.filter(
            weekly_assistance=self.weekly_assistance
        )
        extra_unpaid_hours = sum([
            assistance.extra_unpaid_hours for assistance in assistances
        ])
        extra_hours_base_amount = extra_unpaid_hours * self.get_hour_rate()
        extra_hours_amount = extra_hours_base_amount * settings.EXTRA_HOUR_RATE
        extra_hours_amount_fixed = int(extra_hours_amount * 100) / 100
        return extra_hours_amount_fixed
    
    @property
    def subtotal(self) -> float:
        """ get the subtotal of the payroll:
            weekly rate + no attendance penalty + bonuses +
            other extras + extra unpaid hours
        
        Returns:
            float: Subtotal of the payroll
        """
        subtotal = float(self.weekly_rate)
        subtotal += float(self.no_attendance_penalty)
        subtotal += float(self.penalties_amount)
        subtotal += float(self.bonuses_amount)
        subtotal += float(self.other_amount)
        subtotal += float(self.extra_unpaid_hours_amount)
        
        if subtotal < 0:
            return 0
        
        return int(subtotal * 100) / 100
    
    @property
    def discount_amount(self) -> float:
        """ get the total amount of the discounts
        
        Returns:
            float: Total amount of the discounts
        """
        return - self.__get_extras_amount__('Descuento por robo o daño')
    
    @property
    def location(self) -> str:
        """ get the location of the service agreement
        
        Returns:
            str: Location of the service agreement
        """
        return self.weekly_assistance.service.location
    
    @property
    def bank(self) -> str:
        """ get the bank of the employee
        
        Returns:
            str: Bank of the employee
        """
        return str(self.weekly_assistance.service.employee.bank)
    
    @property
    def card_number(self) -> str:
        """ get the card number of the employee
        
        Returns:
            str: Card number of the employee
        """
        return self.weekly_assistance.service.employee.card_number
    
    @property
    def total(self) -> float:
        """ get the total amount of the payroll
        
        Returns:
            float: Total amount of the payroll
        """
        total = float(self.subtotal)
        total += float(self.discount_amount)
        total += float(self.discount_loans)
        total = int(total * 100) / 100
        if total < 0:
            return 0
        return total
    
    @property
    def week_number(self) -> int:
        """ get the week number of the payroll
        
        Returns:
            int: Week number of the payroll
        """
        
        return self.weekly_assistance.week_number
    
    # Custom name for properties
    agreement_name.fget.short_description = 'Servicio'
    employee_name.fget.short_description = 'Empleado'
    weekly_rate.fget.short_description = 'Salario semanal'
    daily_rate.fget.short_description = 'Salario diario'
    worked_days.fget.short_description = 'Días trabajados'
    no_attendance_days.fget.short_description = 'Faltas'
    no_attendance_penalty.fget.short_description = 'Penalización por faltas'
    penalties_amount.fget.short_description = 'Otras penalizaciones'
    bonuses_amount.fget.short_description = 'Bonos'
    other_amount.fget.short_description = 'Otros'
    extra_unpaid_hours_amount.fget.short_description = 'Horas extras'
    subtotal.fget.short_description = 'Subtotal'
    discount_amount.fget.short_description = 'Descuentos por robo o daño'
    location.fget.short_description = 'Ubicación'
    bank.fget.short_description = 'Banco'
    card_number.fget.short_description = 'Número de tarjeta'
    total.fget.short_description = 'A pagar'
    
    
class PayrollSummary(Payroll):
    class Meta:
        proxy = True
        verbose_name = 'Resumen de nómina'
        verbose_name_plural = 'Resúmenes de nómina'
        
    def __str__(self):
        return f'(Resumen) {self.weekly_assistance}'