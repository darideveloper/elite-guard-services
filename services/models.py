from django.db import models
from django.utils import timezone
from employees.models import Employee


class Schedule(models.Model):
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
        verbose_name='Salario diario sugerido',
        null=True,
        blank=True
    )
    extra_hour_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio por hora extra sugerido',
        null=True,
        blank=True
    )
    bonuses = models.TextField(
        verbose_name='Bonificaciones sugeridas',
        null=True,
        blank=True
    )
    profile_requirements = models.TextField(
        verbose_name='Requisitos de perfil',
        null=True,
        blank=True
    )
    docs_requirements = models.TextField(
        verbose_name='Documentos requeridos',
        null=True,
        blank=True
    )
    uniforms = models.TextField(
        verbose_name='Uniformes',
        null=True,
        blank=True
    )
    safety_equipment = models.TextField(
        verbose_name='Equipo de seguridad',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        
    def __str__(self):
        return f"{self.company_name} (vigencia: {self.effective_date})"
    
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
        Schedule,
        on_delete=models.CASCADE,
        verbose_name='Horario'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    location = models.CharField(
        max_length=150,
        verbose_name='Ubicación'
    )
    description = models.TextField(
        verbose_name='Descripción'
    )
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        
    def __str__(self):
        employee_full_name = f"{self.employee.name} {self.employee.last_name_1}"
        return f"{self.agreement.company_name} - {employee_full_name}"
    
    
    
    
    