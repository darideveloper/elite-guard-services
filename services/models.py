from django.db import models
from django.utils import timezone
from employees.models import Employee


class Schedules(models.Model):
    """ Service schedules model """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    start_time = models.TimeField(
        verbose_name='Hora de inicio'
    )
    end_time = models.TimeField(
        verbose_name='Hora de fin'
    )
    
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        
    def __str__(self):
        return self.name


class Agreement(models.Model):
    """ Company agreements model """
    
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la empresa'
    )
    responsible_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del responsable'
    )
    responsible_phone = models.CharField(
        max_length=15,
        verbose_name='Teléfono del responsable'
    )
    start_date = models.DateField(
        verbose_name='Fecha del acuerdo',
        default=timezone.now
    )
    effective_date = models.DateField(
        verbose_name='Fecha de vigencia'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salario diario sugerido'
    )
    extra_hour_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio por hora extra sugerido'
    )
    bonuses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Bonificaciones sugeridas'
    )
    profile_requirements = models.TextField(
        verbose_name='Requisitos de perfil'
    )
    docs_requirements = models.TextField(
        verbose_name='Documentos requeridos'
    )
    uniforms = models.TextField(
        verbose_name='Uniformes'
    )
    safety_equipment = models.TextField(
        verbose_name='Equipo de seguridad'
    )
    
    class Meta:
        verbose_name = 'Acuerdo'
        verbose_name_plural = 'Acuerdos'
        
    def __str__(self):
        return f"{self.company_name} - {self.effective_date}"
    
    def get_services(self):
        return Service.objects.filter(agreement=self)
    
    def get_employees(self):
        return Employee.objects.filter(service__agreement=self)
    

class Service(models.Model):
    """ Company security services model """
    
    id = models.AutoField(primary_key=True)
    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        verbose_name='Acuerdo'
    )
    schedule = models.ForeignKey(
        Schedules,
        on_delete=models.CASCADE,
        verbose_name='Horario'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    description = models.TextField(
        verbose_name='Descripción'
    )
    location = models.TextField(
        verbose_name='Ubicación'
    )
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        
    def __str__(self):
        employee_full_name = f"{self.employee.name} {self.employee.last_name_1}"
        return f"{self.agreement.company_name} - {employee_full_name}"
    
    
    
    
    