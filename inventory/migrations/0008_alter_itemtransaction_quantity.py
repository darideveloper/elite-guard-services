# Generated by Django 4.2.7 on 2025-01-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_itemloan_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtransaction',
            name='quantity',
            field=models.IntegerField(help_text='(+) Entrada, (-) Salida', verbose_name='Cantidad de transacción'),
        ),
    ]
