# Generated by Django 4.2.7 on 2025-02-03 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_itemtransaction_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemloan',
            options={'verbose_name': 'Préstamo', 'verbose_name_plural': 'Préstamos'},
        ),
        migrations.AlterModelOptions(
            name='itemtransaction',
            options={'verbose_name': 'Transacción', 'verbose_name_plural': 'Transacciones'},
        ),
    ]
