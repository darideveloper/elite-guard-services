from django.db import models

from employees.models import Employee
from services.models import Service


class Item(models.Model):
    """ Main data of items """
    uuid = models.CharField(
        primary_key=True,
        max_length=36,
        verbose_name='UUID',
        help_text='Clave única (no editable después de la creación)',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Precio unitario',
    )
    stock = models.PositiveIntegerField(
        verbose_name='Cantidad en inventario',
        default=1,
        help_text='No editable después de la creación (añadir transacciones)',
    )
    details = models.TextField(
        verbose_name='Detalles',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        
    def __str__(self):
        return f"{self.uuid} ({self.name})"
    
    def save(self, *args, **kwargs):
        # TODO: Create ItemsStock object if it does not exist
        
        super(Item, self).save(*args, **kwargs)
        
        
class ItemTransaction(models.Model):
    """ Transactions of items (in/out) """
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Cantidad de transacción',
        help_text='(+) Entrada, (-) Salida'
    )
    details = models.TextField(
        verbose_name='Detalles',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transacción de Artículo'
        verbose_name_plural = 'Transacciones de Artículos'
        
    def __str__(self):
        return f"{self.item.name} - transaction {self.quantity}"
    
    def save(self, *args, **kwargs):
        # TODO: no update quantity
        
        # TODO: validate item stock
        
        # TODO: Update item stock
        
        super(ItemTransaction, self).save(*args, **kwargs)
    
    
class ItemLoan(models.Model):
    """ Loans of items to employees in specific services """
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Artículo'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Cantidad de préstamo',
    )
    details = models.TextField(
        verbose_name='Detalles',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Préstamo de Artículo'
        verbose_name_plural = 'Préstamos de Artículos'
        
    def __str__(self):
        return f"{self.item.name} - loan {self.quantity}"
    
    def save(self, *args, **kwargs):
        # TODO: no update quantity
        
        # TODO: validate item stock
        
        # TODO: Add ItemTransaction
        
        # TODO: Create Loan
        
        super(ItemLoan, self).save(*args, **kwargs)