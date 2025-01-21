from django.contrib import admin
from inventory import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'name',
        'price',
        'stock',
        # 'total_price',
    )
    search_fields = (
        'name',
        'details',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    # TODO: custom field: total_price
    

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