from django.db import models
from employees import models as employees_models
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
    employee = models.ForeignKey(
        employees_models.Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    work_days = models.IntegerField(
        verbose_name='Días trabajados'
    )
    no_attendance_days = models.IntegerField(
        verbose_name='Días no laborados'
    )
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Sub total',
        default=0
    )
    
    class Meta:
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nóminas'
        
    def __str__(self):
        return f'{self.employee} - {self.weekly_assistance}'
    
    