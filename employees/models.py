from django.db import models
from django.utils import timezone


class Colony(models.Model):
    """ Secondary model for employee colony """
    
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
    
    # TODO: service
    
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
        blank=True,
        null=True
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Peso',
        help_text='Peso en kilogramos',
        blank=True,
        null=True
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
    
    # Birth info
    birthdate = models.DateField(
        verbose_name='Fecha de nacimiento'
    )
    municipality_birth = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        verbose_name='Lugar de nacimiento',
        help_text='Estado y municipio de nacimiento',
        related_name='municipality_birth'
    )
    
    # Work info
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Slario diario'
    )
    curp = models.CharField(
        max_length=18,
        verbose_name='CURP',
        help_text='Clave Única de Registro de Población'
    )
    rfc = models.CharField(
        max_length=13,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes',
        blank=True,
        null=True
    )
    imss = models.CharField(
        max_length=11,
        verbose_name='IMSS',
        help_text='Instituto Mexicano del Seguro Social',
        blank=True,
        null=True
    )
    infonavit = models.CharField(
        max_length=11,
        verbose_name='INFONAVIT',
        help_text='Instituto del Fondo Nacional de la Vivienda para los Trabajadores',
        blank=True,
        null=True
    )
    ine = models.CharField(
        max_length=13,
        verbose_name='INE',
        help_text='Número de credencial de Instituto Nacional Electoral'
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
    colony = models.ForeignKey(
        Colony,
        on_delete=models.PROTECT,
        verbose_name='Colonia'
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
        verbose_name='Teléfono'
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
        null=True
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
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
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificación'
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
        now = timezone.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        # save in status_history the employee status change
        if is_new:
            self.status_history += f"({now_str}) Estado: {self.status}"
        else:
            old_status = self._meta.model.objects.get(pk=self.pk).status
            new_status = self.status
            if old_status != new_status:
                text = f"\n({now_str}) Estado: {old_status} >>> {new_status}"
                if self.status_change_details:
                    text += f" - Detalles: {self.status_change_details}"
                self.status_history += text

        # Save the employee
        super(Employee, self).save(*args, **kwargs)
    
    def get_age(self):
        """ Calculate employee age """
        today = timezone.now()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )
    
# TODO: EmployeeInventory related models


class WeeklyLoan(models.Model):
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
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Préstamo semanal'
        verbose_name_plural = 'Préstamos semanales'
        
    def __str__(self):
        """ Text representation """
        return f"{self.employee} ({self.amount})"

    def save(self, *args, **kwargs):
        """ Custom save method """
        
        # update employee balance when save a wekly loan
        self.employee.balance += self.amount
        self.employee.save()
        
        # Save the wekly loan
        super(WeeklyLoan, self).save(*args, **kwargs)
       
        
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
    
    