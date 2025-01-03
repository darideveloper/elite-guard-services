# Generated by Django 4.2.7 on 2024-12-20 00:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agreement',
            options={'verbose_name': 'Acuerdo con empresa', 'verbose_name_plural': 'Acuerdos con empresas'},
        ),
        migrations.AlterModelOptions(
            name='schedules',
            options={'verbose_name': 'Horario', 'verbose_name_plural': 'Horarios'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Servicio', 'verbose_name_plural': 'Servicios'},
        ),
        migrations.AddField(
            model_name='agreement',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha del acuerdo'),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Salario diario sugerido'),
        ),
    ]
