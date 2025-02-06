from django.db import models

from employees.models import Employee, Loan
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
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        
    def __str__(self):
        return f"{self.name} ({self.uuid}) - En stock: {self.stock}"
        
        
class ItemTransaction(models.Model):
    """ Transactions of items (in/out) """
    
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        verbose_name='Cantidad de transacción',
        help_text='(+) Entrada, (-) Salida'
    )
    details = models.TextField(
        verbose_name='Detalles',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        
    def __str__(self):
        return f"{self.item.name} - transaction {self.quantity}"
    
    def save(self, *args, **kwargs):
                
        # validate item stock
        is_nevagitve = self.item.stock + self.quantity < 0
        if is_nevagitve:
            raise ValueError(
                'No hay suficiente stock para la transacción. '
                f'Stock actual: {self.item.stock}'
            )
        
        # Update item stock
        self.item.stock += self.quantity
        self.item.save()
        
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
    details = models.TextField(
        verbose_name='Detalles',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        
    def __str__(self):
        return f"{self.item.name} - loan {self.quantity}"
    
    def save(self, *args, **kwargs):
        
        # No edit after creation
        if self.pk:
            raise ValueError('No se puede editar un préstamo')
                
        # validate item stock
        is_nevagitve = self.item.stock - self.quantity < 0
        if is_nevagitve:
            raise ValueError(
                'No hay suficiente stock para el préstamo. '
                f'Stock actual: {self.item.stock}'
            )
        
        # Add ItemTransaction
        ItemTransaction.objects.create(
            item=self.item,
            quantity=-self.quantity,
            details=f"<<Prestamo>>: empleado: {self.employee} "
                    f"- servicio: {self.service} - detalles: {self.details}",
        )
        
        # Create Loan
        Loan.objects.create(
            employee=self.employee,
            amount=self.item.price * self.quantity,
            details=f"<<Préstamo>>: item: {self.item} - cantidad: {self.quantity} "
                    f"- servicio: {self.service} - detalles: {self.details}",
        )
        
        super(ItemLoan, self).save(*args, **kwargs)