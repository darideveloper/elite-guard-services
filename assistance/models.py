from django.utils import timezone

from django.db import models
from services import models as services_models
from utils.dates import get_week_day, get_current_week


class Assistance(models.Model):
    """ Employee assistance model """

    id = models.AutoField(primary_key=True)
    date = models.DateField(
        verbose_name='Fecha',
        default=timezone.now
    )
    attendance = models.BooleanField(
        verbose_name='Asistencia',
        default=False
    )
    extra_paid_hours = models.IntegerField(
        verbose_name='Hrs extras pagadas',
        default=0
    )
    extra_unpaid_hours = models.IntegerField(
        verbose_name='Hrs no pagadas',
        default=0
    )
    notes = models.TextField(
        verbose_name='Notas',
        null=True,
        blank=True
    )
    weekly_assistance = models.ForeignKey(
        'WeeklyAssistance',
        on_delete=models.CASCADE,
        verbose_name='Asistencia semanal',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Fecha de creación',
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        verbose_name='Fecha de actualización',
        default=timezone.now
    )

    class Meta:
        verbose_name = 'Asistencia diaria'
        verbose_name_plural = 'Asistencias diarias'

    def __str__(self):
        return f"{self.date} - {self.weekly_assistance}"

    def save(self, *args, **kwargs):
        
        # Update weekly assistance data when change
        if (self.id):

            # Update weekday status
            day_name = get_week_day(self.date, "en")
            setattr(self.weekly_assistance, day_name, self.attendance)
            super(Assistance, self).save(*args, **kwargs)
            
            # Update weekly paid hours
            all_weekly_assistances = Assistance.objects.filter(
                weekly_assistance=self.weekly_assistance
            )
            self.weekly_assistance.total_extra_paid_hours = sum(
                [assistance.extra_paid_hours for assistance in all_weekly_assistances]
            )
            
            # Update weekly unpaid hours
            self.weekly_assistance.total_extra_unpaid_hours = sum(
                [assistance.extra_unpaid_hours for assistance in all_weekly_assistances]
            )
            
            # Update comments
            all_comments = [
                assistance.notes for assistance in all_weekly_assistances
            ]
            all_comments = list(filter(lambda note: note is not None, all_comments))
            self.weekly_assistance.notes = "\n".join(all_comments)
            
        # Save the object
        self.weekly_assistance.save()
        super(Assistance, self).save(*args, **kwargs)


class WeeklyAssistance(models.Model):
    """ Employee weekly assistance model """

    service = models.ForeignKey(
        services_models.Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )
    week_number = models.IntegerField(
        verbose_name='Número de semana',
    )
    start_date = models.DateField(
        verbose_name='Fecha de inicio',
    )
    end_date = models.DateField(
        verbose_name='Fecha de fin',
    )
    thursday = models.BooleanField(
        verbose_name='Jueves',
        default=False
    )
    friday = models.BooleanField(
        verbose_name='Viernes',
        default=False
    )
    saturday = models.BooleanField(
        verbose_name='Sábado',
        default=False
    )
    sunday = models.BooleanField(
        verbose_name='Domingo',
        default=False
    )
    monday = models.BooleanField(
        verbose_name='Lunes',
        default=False
    )
    tuesday = models.BooleanField(
        verbose_name='Martes',
        default=False
    )
    wednesday = models.BooleanField(
        verbose_name='Miércoles',
        default=False
    )
    total_extra_paid_hours = models.IntegerField(
        verbose_name='Horas extras pagadas',
        default=0
    )
    total_extra_unpaid_hours = models.IntegerField(
        verbose_name='Horas extras no pagadas',
        default=0
    )
    notes = models.TextField(
        verbose_name='Notas',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Asistencia semanal'
        verbose_name_plural = 'Asistencias semanales'

    def __str__(self):
        return f"{self.service} - Semana {self.week_number}"
    
    def save(self, *args, **kwargs):
        """ Calculate default values """
        
        # Calculate dates
        self.start_date = timezone.now().astimezone()
        self.end_date = self.start_date + timezone.timedelta(days=6)
        self.week_number = get_current_week(self.start_date)
        
        super(WeeklyAssistance, self).save(*args, **kwargs)
    
    def get_data_header(self):
        
        return ([
            "Contrato",
            "Empleado",
            "J",
            "V",
            "S",
            "D",
            "L",
            "M",
            "X",
            "Turnos",
            "Extra pagadas",
            "Extra no pagadas",
            "Comentarios"
        ])
    
    def get_data_list(self):
        
        return ([
            self.service.agreement.company_name,
            self.service.employee.get_full_name(),
            "a" if self.thursday else "f",
            "a" if self.friday else "f",
            "a" if self.saturday else "f",
            "a" if self.sunday else "f",
            "a" if self.monday else "f",
            "a" if self.tuesday else "f",
            "a" if self.wednesday else "f",
            sum([
                self.thursday,
                self.friday,
                self.saturday,
                self.sunday,
                self.monday,
                self.tuesday,
                self.wednesday
            ]),
            self.total_extra_paid_hours,
            self.total_extra_unpaid_hours,
            self.notes
        ])
        
    def get_is_highlighted(self) -> bool:
        """ get if the weekly assistance is highlighted
        (no highlighted by default)
        
        Returns:
            bool: always False
        """
        return False
        
    def get_day_assistance(self, day: str) -> bool:
        """ Get the assistance of the day

        Args:
            day (str): Day of the week (e.g. 'monday')

        Returns:
            bool: True if the employee attended, False otherwise
        """
        
        return getattr(self, day)
    
    def get_worked_days(self) -> int:
        """ Get the number of days worked in the week

        Returns:
            int: Number of days worked
        """
        
        return sum([
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday,
            self.monday,
            self.tuesday,
            self.wednesday
        ])
        
    def get_no_attendance_days(self) -> int:
        """ Get the number of days without attendance in the week

        Returns:
            int: Number of days without attendance
        """
        
        weekly_attendances = self.service.schedule.weekly_attendances
        work_days = self.get_worked_days()
        no_attendances = weekly_attendances - work_days
        if no_attendances < 0:
            return 0
        return weekly_attendances - work_days
    

class ExtraPaymentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='Nombre',
        max_length=100
    )
    description = models.TextField(
        verbose_name='Descripción',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Categoría de extra'
        verbose_name_plural = 'Categorías de extras'
        
    def __str__(self):
        return self.name


class ExtraPayment(models.Model):
    id = models.AutoField(primary_key=True)
    assistance = models.ForeignKey(
        Assistance,
        on_delete=models.CASCADE,
        verbose_name='Asistencia'
    )
    category = models.ForeignKey(
        ExtraPaymentCategory,
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )
    amount = models.DecimalField(
        verbose_name='Monto',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Monto del extra (sieempre positivo +)'
    )
    notes = models.TextField(
        verbose_name='Notas',
        default=''
    )
    created_at = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Fecha de actualización',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Extra'
        verbose_name_plural = 'Extras'
    
    def __str__(self):
        employee = self.assistance.weekly_assistance.service.employee
        return f"{employee} - {self.category.name}"
    