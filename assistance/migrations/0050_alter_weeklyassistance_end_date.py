# Generated by Django 4.2.7 on 2025-02-04 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0049_alter_weeklyassistance_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyassistance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2025, 2, 10, 14, 52, 19, 412854, tzinfo=datetime.timezone.utc), verbose_name='Fecha de fin'),
        ),
    ]
