# Generated by Django 4.2.7 on 2024-12-24 23:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0013_alter_assistance_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistance',
            name='weekly_assistance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assistance.weeklyassistance', verbose_name='Asistencia semanal'),
        ),
        migrations.AlterField(
            model_name='weeklyassistance',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 30, 23, 41, 39, 559775, tzinfo=datetime.timezone.utc), verbose_name='Fecha de fin'),
        ),
    ]