# Generated by Django 4.2.7 on 2025-02-06 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0055_alter_assistance_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistance',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notas'),
        ),
    ]
