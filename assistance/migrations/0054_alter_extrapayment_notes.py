# Generated by Django 4.2.7 on 2025-02-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0053_alter_weeklyassistance_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrapayment',
            name='notes',
            field=models.TextField(default='', verbose_name='Notas'),
        ),
    ]
