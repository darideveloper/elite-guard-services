from django.db import models


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
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
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
    

class Employee(models.Model):
    """ Primary model for employees """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Apellido'
    )
    # TODO: service
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Slario diario'
    )
    born_date = models.DateField(
        verbose_name='Fecha de nacimiento'
    )
    curp = models.CharField(
        max_length=18,
        verbose_name='CURP',
        help_text='Clave Única de Registro de Población'
    )
    rfc = models.CharField(
        max_length=13,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes'
    )
    imss = models.CharField(
        max_length=11,
        verbose_name='IMSS',
        help_text='Instituto Mexicano del Seguro Social'
    )
    infonavit = models.CharField(
        max_length=11,
        verbose_name='INFONAVIT',
        help_text='Instituto del Fondo Nacional de la Vivienda para los Trabajadores'
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
        verbose_name='Estado civil'
    )
    colony = models.ForeignKey(
        Colony,
        on_delete=models.PROTECT,
        verbose_name='Colonia'
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        verbose_name='Municipio'
    )
    postal_code = models.CharField(
        max_length=5,
        verbose_name='Código postal'
    )
    address = models.TextField(
        verbose_name='Domicilio'
    )
    phone = models.CharField(
        max_length=10,
        verbose_name='Teléfono'
    )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        verbose_name='Banco',
        help_text='Banco donde se deposita el salario'
    )
    card_number = models.CharField(
        max_length=16,
        verbose_name='Número de tarjeta',
        help_text='Número de tarjeta de débito o nómina'
    )
    uniform_date = models.DateField(
        verbose_name='Fecha de uniforme',
        help_text='Fecha de entrega de uniforme'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Estatus'
    )
    anti_doping_results = models.TextField(
        verbose_name='Resultados de antidoping'
    )
    administrative_violations = models.IntegerField(
        verbose_name='Infracciones administrativas',
        help_text='Número de infracciones administrativas hasta la fecha'
    )
    administrative_comments = models.TextField(
        verbose_name='Comentarios administrativos',
        help_text='Detalles de las infracciones administrativas'
    )
    status_history = models.TextField(
        verbose_name='Historial de estatus',
        help_text='Historial de estatus (activo, inactivo, baja, etc). Autollenado'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Saldo de préstamos'
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
        
        # TODO: save in status_history the employee register
        # TODO: save in status_history the employee set to active
        # TODO: save in status_history the employee set to inactive
        
        # Save the employee
        super(Employee, self).save(*args, **kwargs)
    
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
        
        # TODO: update employee balance when save a wekly loan
        
        # Save the wekly loan
        super(WeeklyLoan, self).save(*args, **kwargs)