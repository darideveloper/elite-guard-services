from django.utils import timezone

from django.db import models
from services import models as services_models


class Assistance(models.Model):
    """ Employee assistance in services model """
    
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
    