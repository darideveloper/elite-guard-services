# Generated by Django 4.2.7 on 2025-01-10 04:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0018_weeklyassistance_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyassistance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2025, 1, 16, 4, 25, 45, 661615, tzinfo=datetime.timezone.utc), verbose_name='Fecha de fin'),
        ),
    ]