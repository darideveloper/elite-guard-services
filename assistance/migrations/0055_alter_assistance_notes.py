# Generated by Django 4.2.7 on 2025-02-06 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0054_alter_extrapayment_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistance',
            name='notes',
            field=models.TextField(default='', verbose_name='Notas'),
        ),
    ]
