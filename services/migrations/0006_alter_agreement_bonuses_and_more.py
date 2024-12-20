# Generated by Django 4.2.7 on 2024-12-20 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_agreement_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='bonuses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Bonificaciones sugeridas'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='docs_requirements',
            field=models.TextField(blank=True, null=True, verbose_name='Documentos requeridos'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='extra_hour_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio por hora extra sugerido'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='profile_requirements',
            field=models.TextField(blank=True, null=True, verbose_name='Requisitos de perfil'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='safety_equipment',
            field=models.TextField(blank=True, null=True, verbose_name='Equipo de seguridad'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salario diario sugerido'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='uniforms',
            field=models.TextField(blank=True, null=True, verbose_name='Uniformes'),
        ),
    ]