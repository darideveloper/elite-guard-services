from django.utils import timezone

from django.db import models
from services import models as services_models


class Assistance(models.Model):
    """ Employee assistance model """
    
    id = models.AutoField(primary_key=True)
    date = models.DateField(
        verbose_name='Fecha',
        default=timezone.now
    )
    service = models.ForeignKey(
        services_models.Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )
    attendance = models.BooleanField(
        verbose_name='Asistencia'
    )
    extra_paid_hours = models.IntegerField(
        verbose_name='Horas extras pagadas',
        default=0
    )
    extra_unpaid_hours = models.IntegerField(
        verbose_name='Horas extras no pagadas',
        default=0
    )
    notes = models.TextField(
        verbose_name='Notas',
        default=''
    )
    
    class Meta:
        verbose_name = 'Asistencia diaria'
        verbose_name_plural = 'Asistencias diarias'
        
    def __str__(self):
        return f"{self.date} - {self.service}"
    

class WeeklyAssistance(models.Model):
    """ Employee weekly assistance model """
    
    service = models.ForeignKey(
        services_models.Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )
    week_number = models.IntegerField(
        verbose_name='Número de semana',
        default=timezone.now().isocalendar()[1]
    )
    start_date = models.DateField(
        verbose_name='Fecha de inicio',
        default=timezone.now
    )
    end_date = models.DateField(
        verbose_name='Fecha de fin',
        default=timezone.now() + timezone.timedelta(days=6)
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
    total_extra_paid_hours = models.IntegerField(
        verbose_name='Horas extras pagadas',
        default=0
    )
    total_extra_unpaid_hours = models.IntegerField(
        verbose_name='Horas extras no pagadas',
        default=0
    )
    
    class Meta:
        verbose_name = 'Asistencia semanal'
        verbose_name_plural = 'Asistencias semanales'
        
    def __str__(self):
        return f"{self.service} - Semana {self.week_number}"