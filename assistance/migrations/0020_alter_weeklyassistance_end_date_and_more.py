# Generated by Django 4.2.7 on 2025-01-21 17:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0019_alter_weeklyassistance_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyassistance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2025, 1, 27, 17, 4, 6, 939603, tzinfo=datetime.timezone.utc), verbose_name='Fecha de fin'),
        ),
        migrations.AlterField(
            model_name='weeklyassistance',
            name='week_number',
            field=models.IntegerField(default=3, verbose_name='Número de semana'),
        ),
    ]
