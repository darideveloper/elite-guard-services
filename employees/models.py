from django.db import models
from django.utils import timezone

import random


class Neighborhood(models.Model):
    """ Secondary model for employee neighborhood """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la colonia'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Colonia'
        verbose_name_plural = 'Colonias'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Municipality(models.Model):
    """ Secondary model for employee municipality """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del municipio'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    

class MaritalStatus(models.Model):
    """ Secondary model for employee marital status """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del estado civil'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Estado Civil'
        verbose_name_plural = 'Estados Civiles'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name


class Status(models.Model):
    """ Secondary model for employee status """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del estado'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Estatus de empleado'
        verbose_name_plural = 'Estatus de empleados'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name


class Bank(models.Model):
    """ Secondary model for employee bank """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del banco'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Education(models.Model):
    """ Secondary model for employee education """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del nivel educación'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Educación'
        verbose_name_plural = 'Educaciones'
        ordering = ['id']
        
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Language(models.Model):
    """ Secondary model for employee language """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del idioma'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Employee(models.Model):
    """ Primary model for employees """
        
    # General info
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre(s)'
    )
    last_name_1 = models.CharField(
        max_length=100,
        verbose_name='Apellido paterno'
    )
    last_name_2 = models.CharField(
        max_length=100,
        verbose_name='Apellido materno',
        blank=True,
        null=True
    )
    height = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name='Estatura',
        help_text='Estatura en metros',
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Peso',
        help_text='Peso en kilogramos',
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
        verbose_name='Estado civil'
    )
    education = models.ForeignKey(
        Education,
        on_delete=models.PROTECT,
        verbose_name='Nivel de educación'
    )
    languages = models.ManyToManyField(
        Language,
        verbose_name='Idiomas'
    )
    photo = models.ImageField(
        upload_to='employees/photos/',
        verbose_name='Foto',
        help_text='Fotografía del empleado (tamaño recomendado: 300x300px)',
        blank=True,
        null=True
    )
    code = models.CharField(max_length=6, unique=True, editable=False)

    # Birth info
    birthdate = models.DateField(
        verbose_name='Fecha de nacimiento'
    )
    municipality_birth = models.CharField(
        max_length=100,
        verbose_name='Lugar de nacimiento'
    )
    
    # Work info
    weekly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salario semanal'
    )
    curp = models.CharField(
        max_length=18,
        verbose_name='CURP',
        help_text='Clave Única de Registro de Población',
        unique=True
    )
    rfc = models.CharField(
        max_length=13,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes',
        blank=True,
        null=True,
        unique=True
    )
    imss = models.CharField(
        max_length=11,
        verbose_name='IMSS',
        help_text='Instituto Mexicano del Seguro Social',
        blank=True,
        null=True,
        unique=True
    )
    infonavit = models.CharField(
        max_length=11,
        verbose_name='INFONAVIT',
        help_text='Instituto del Fondo Nacional de la Vivienda para los Trabajadores',
        blank=True,
        null=True,
        unique=True
    )
    ine = models.CharField(
        max_length=13,
        verbose_name='INE',
        help_text='Número de credencial de Instituto Nacional Electoral',
        unique=True
    )
    uniform_date = models.DateField(
        verbose_name='Fecha de uniforme',
        help_text='Fecha de entrega de uniforme',
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Estatus de empleado',
        default=1
    )
    status_change_details = models.TextField(
        verbose_name='Detalles de cambio de estatus',
        help_text='Detalles del cambio de estatus',
        blank=True,
        null=True
    )
    knowledge = models.TextField(
        verbose_name='Conocimientos',
        help_text='Conocimientos y experiencia del empleado'
    )
    skills = models.TextField(
        verbose_name='Habilidades',
        help_text='Habilidades y destrezas del empleado'
    )
    
    # Contact info
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        verbose_name='Lugar de residencia',
        help_text='Estado y municipio de residencia'
    )
    neighborhood = models.ForeignKey(
        Neighborhood,
        on_delete=models.PROTECT,
        verbose_name='Colonia',
    )
    postal_code = models.CharField(
        max_length=5,
        verbose_name='Código postal'
    )
    address_street = models.CharField(
        max_length=100,
        verbose_name='Calle de residencia'
    )
    address_number = models.CharField(
        max_length=10,
        verbose_name='Número de residencia',
        help_text='Número de la casa o departamento'
    )
    phone = models.CharField(
        max_length=10,
        verbose_name='Teléfono',
        unique=True
    )
    emergency_phone = models.CharField(
        max_length=10,
        verbose_name='Teléfono de emergencia'
    )
    
    # Bank info
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        verbose_name='Banco',
        help_text='Banco donde se deposita el salario',
        blank=True,
        null=True
    )
    card_number = models.CharField(
        max_length=16,
        verbose_name='Número de tarjeta',
        help_text='Número de tarjeta de débito o nómina',
        blank=True,
        null=True,
        unique=True
    )
    balance = models.FloatField(
        verbose_name='Saldo de préstamos',
        default=0
    )
    
    # Other info
    anti_doping_results = models.TextField(
        verbose_name='Resultados de antidoping',
        default='Sin resultados de antidoping'
    )
    administrative_violations = models.IntegerField(
        verbose_name='Infracciones administrativas',
        help_text='Número de infracciones administrativas hasta la fecha',
        default=0
    )
    administrative_comments = models.TextField(
        verbose_name='Comentarios administrativos',
        help_text='Detalles de las infracciones administrativas',
        blank=True,
        null=True
    )
    status_history = models.TextField(
        verbose_name='Historial de estatus',
        help_text='Historial de estatus (activo, inactivo, baja, etc). Autollenado',
        default=''
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de ingreso',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última modificación'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        
    def __str__(self):
        """ Text representation """
        return f"{self.name} ({self.curp})"
    
    def save(self, *args, **kwargs):
        """ Custom save method """
        
        is_new = self._state.adding
        now = timezone.now().astimezone()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
                
        # save in status_history the employee status change
        if is_new:
            self.status_history += f"({now_str}) Estado: {self.status}"
            
            # Generate unique code
            self.code = self.generate_unique_code()
        else:
            
            # Import services models avoiding circular imports
            from services import models as services_models
            
            # Get current emoloyee service
            employee_services = services_models.Service.objects.filter(
                employee=self.pk
            )
            if employee_services:
                employee_service = employee_services.order_by('-id').first()
            else:
                employee_service = None
            
            # Generate new status log
            old_status = self._meta.model.objects.get(pk=self.pk).status
            new_status = self.status
            if old_status != new_status:
                text = f"\n({now_str}) Estado: {old_status} >>> {new_status}"
                if self.status_change_details:
                    text += f" - Detalles: {self.status_change_details}"
                if employee_service:
                    text += f" - Servicio: {employee_service.agreement.company_name}"
                self.status_history += text
                
            # Reset status change details
            self.status_change_details = ''

        # Save the employee
        super(Employee, self).save(*args, **kwargs)
    
    def generate_unique_code(self):
        while True:
            code = "{:06d}".format(random.randint(0, 999999))
            if not Employee.objects.filter(code=code).exists():
                return code
    
    def get_age(self):
        """ Calculate employee age """
        today = timezone.now()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )
        
    def get_full_name(self):
        """ Return the full name of the employee
        
        Returns:
            str: Full name of the employee
        """
        
        full_name = f"{self.name} {self.last_name_1}"
        if self.last_name_2:
            full_name += f" {self.last_name_2}"
        return full_name
    

class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Monto',
        help_text='Monto pedido (-) o pagado (+)'
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de prestamo o pago'
    )
    details = models.TextField(
        verbose_name='Detalles',
        help_text='Detalles del préstamo o pago',
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        
    def __str__(self):
        """ Text representation """
        return f"{self.employee} ({self.amount})"

    def save(self, *args, **kwargs):
        """ Custom save method """
        
        # update employee balance when save a wekly loan
        self.employee.balance += float(self.amount)
        self.employee.save()
        
        # Save the wekly loan
        super(Loan, self).save(*args, **kwargs)
       
        
class Ref(models.Model):
    """ Reference model """
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de referencia'
    )
    phone = models.CharField(
        max_length=10,
        verbose_name='Teléfono de referencia'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Referencia'
        verbose_name_plural = 'Referencias'
        
    def __str__(self):
        """ Text representation """
        return f"{self.name} ({self.employee})"
    
    
class Relationship(models.Model):
    """ Secondary model for relative relationship with employee """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de relación'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Parentesco'
        verbose_name_plural = 'Parentescos'
        ordering = ['name']
    
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Relative(models.Model):
    """ Relative model """
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de familiar'
    )
    last_name_1 = models.CharField(
        max_length=100,
        verbose_name='Apellido paterno'
    )
    last_name_2 = models.CharField(
        max_length=100,
        verbose_name='Apellido materno',
        null=True,
        blank=True
    )
    relationship = models.ForeignKey(
        Relationship,
        on_delete=models.PROTECT,
        verbose_name='Parentesco'
    )
    phone = models.CharField(
        max_length=10,
        verbose_name='Teléfono de familiar'
    )
    age = models.IntegerField(
        verbose_name='Edad de familiar'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Familiar'
        verbose_name_plural = 'Familiares'
    
    def __str__(self):
        """ Text representation """
        return f"{self.name} ({self.relationship} - {self.employee})"
    
    