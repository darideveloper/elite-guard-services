from django.db import models


class Colony(models.Model):
    """ Secondary model for employee colony """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre de la colonia'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Colony'
        verbose_name_plural = 'Colonies'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    
    
class Municipality(models.Model):
    """ Secondary model for employee municipality """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre del municipio'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Municipality'
        verbose_name_plural = 'Municipalities'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    

class MaritalStatus(models.Model):
    """ Secondary model for employee marital status """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre del estado civil'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Statuses'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name


class Status(models.Model):
    """ Secondary model for employee status """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre del estado'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Employee Status'
        verbose_name_plural = 'Employee Statuses'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name


class Bank(models.Model):
    """ Secondary model for employee bank """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre del banco'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
        ordering = ['name']
        
    def __str__(self):
        """ Text representation """
        return self.name
    

class Employee(models.Model):
    """ Primary model for employees """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text='Nombre'
    )
    last_name = models.CharField(
        max_length=100,
        help_text='Apellido'
    )
    # TODO: service
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Slario diaria'
    )
    born_date = models.DateField(
        help_text='Fecha de nacimiento'
    )
    curp = models.CharField(
        max_length=18,
        help_text='Clave Única de Registro de Población'
    )
    rfc = models.CharField(
        max_length=13,
        help_text='Registro Federal de Contribuyentes'
    )
    imss = models.CharField(
        max_length=11,
        help_text='Instituto Mexicano del Seguro Social'
    )
    infonavit = models.CharField(
        max_length=11,
        help_text='Instituto del Fondo Nacional de la Vivienda para los Trabajadores'
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
        help_text='Estado civil'
    )
    address = models.TextField(
        help_text='Domicilio'
    )
    colony = models.ForeignKey(
        Colony,
        on_delete=models.PROTECT,
        help_text='Colonia'
    )
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        help_text='Municipio'
    )
    postal_code = models.CharField(
        max_length=5,
        help_text='Código postal'
    )
    phone = models.CharField(
        max_length=10,
        help_text='Teléfono'
    )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        help_text='Banco'
    )
    card_number = models.CharField(
        max_length=16,
        help_text='Número de tarjeta'
    )
    uniform_date = models.DateField(
        help_text='Fecha de entrega de uniforme'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        help_text='Estatus'
    )
    anti_doping_results = models.TextField(
        help_text='Resultados de antidoping'
    )
    administrative_violations = models.IntegerField(
        help_text='Infracciones administrativas'
    )
    administrative_comments = models.TextField(
        help_text='Comentarios administrativos'
    )
    status_history = models.TextField(
        help_text='Historial de estatus (activo, inactivo, baja, etc)'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Saldo de préstamos'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de modificación'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        
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
        help_text='Empleado'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Monto pedido (-) o pagado (+)'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de registro'
    )
    
    class Meta:
        """ Model metadata """
        verbose_name = 'Wekly Loan'
        verbose_name_plural = 'Wekly Loans'
        
    def __str__(self):
        """ Text representation """
        return f"{self.employee} ({self.amount})"

    def save(self, *args, **kwargs):
        """ Custom save method """
        
        # TODO: update employee balance when save a wekly loan
        
        # Save the wekly loan
        super(WeklyLoan, self).save(*args, **kwargs)