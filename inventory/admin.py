from django.contrib import admin, messages
from inventory import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'name',
        'price',
        'stock',
        'total_price',
    )
    search_fields = (
        'name',
        'details',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """ Save model without updating stock """
        
        if change and obj.stock != form.initial['stock']:
            # Show error
            messages.set_level(request, messages.WARNING)
            messages.error(
                request,
                'No se puede modificar el stock de un artículo directamente'
            )
            messages.warning(request, 'Por favor, añada una transacción de artículo')
            
            # Set stock to initial value
            obj.stock = form.initial['stock']
        
        obj.save()
    
    # Custom fields
    def total_price(self, obj):
        """ Return the total price of the item """
        return obj.price * obj.stock
    
    # Labels for custom fields
    total_price.short_description = 'Precio total'
    

@admin.register(models.ItemTransaction)
class ItemTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'quantity',
        'details',
    )
    search_fields = (
        'item__name',
        'item__details',
        'details',
    )
    list_filter = (
        'item',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """ Save model without updating quantity """
            
        # Try to save and show error or confirmation message
        try:
            obj.save()
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, str(e))
        else:
            messages.info(
                request,
                'Stock actualizado'
            )
    

@admin.register(models.ItemLoan)
class ItemLoanAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'employee',
        'service',
        'quantity',
    )
    search_fields = (
        'item__name',
        'item__details',
        'employee__first_name',
        'employee__last_name_1',
        'employee__last_name_2',
        'service__agreement__company_name',
        'service__location',
        'service__description',
    )
    list_filter = (
        'item',
        'employee',
        'service',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """ Save model without updating quantity """
        
        if change and obj.quantity != form.initial['quantity']:
            # Show error
            messages.set_level(request, messages.WARNING)
            messages.error(
                request,
                'No se puede modificar la cantidad de un '
                'préstamo de artículo directamente'
            )
            messages.warning(
                request,
                'Por favor, añada un nuevo préstamo de artículo'
            )
        
            # Set quantity to initial value
            obj.quantity = form.initial['quantity']
            
        # Try to save and show error or confirmation message
        try:
            obj.save()
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, str(e))
        else:
            messages.info(
                request,
                'Stock actualizado'
            )