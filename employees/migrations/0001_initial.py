# Generated by Django 4.2.7 on 2024-12-14 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colony',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nombre de la colonia', max_length=100)),
            ],
            options={
                'verbose_name': 'Colony',
                'verbose_name_plural': 'Colonies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nombre', max_length=100)),
                ('last_name', models.CharField(help_text='Apellido', max_length=100)),
                ('daily_rate', models.DecimalField(decimal_places=2, help_text='Slario diaria', max_digits=10)),
                ('born_date', models.DateField(help_text='Fecha de nacimiento')),
                ('curp', models.CharField(help_text='Clave Única de Registro de Población', max_length=18)),
                ('rfc', models.CharField(help_text='Registro Federal de Contribuyentes', max_length=13)),
                ('imss', models.CharField(help_text='Instituto Mexicano del Seguro Social', max_length=11)),
                ('infonavit', models.CharField(help_text='Instituto del Fondo Nacional de la Vivienda para los Trabajadores', max_length=11)),
                ('address', models.TextField(help_text='Domicilio')),
                ('postal_code', models.CharField(help_text='Código postal', max_length=5)),
                ('phone', models.CharField(help_text='Teléfono', max_length=10)),
                ('bank_name', models.CharField(help_text='Nombre del banco', max_length=100)),
                ('card_number', models.CharField(help_text='Número de tarjeta', max_length=16)),
                ('uniform_date', models.DateField(help_text='Fecha de entrega de uniforme')),
                ('anti_doping_results', models.TextField(help_text='Resultados de antidoping')),
                ('administrative_violations', models.IntegerField(help_text='Infracciones administrativas')),
                ('administrative_comments', models.TextField(help_text='Comentarios administrativos')),
                ('status_history', models.TextField(help_text='Historial de estatus (activo, inactivo, baja, etc)')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha de creación')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Fecha de modificación')),
                ('balance', models.DecimalField(decimal_places=2, help_text='Saldo de préstamos', max_digits=10)),
                ('colony', models.ForeignKey(help_text='Colonia', on_delete=django.db.models.deletion.PROTECT, to='employees.colony')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='EmployeeStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nombre del estado', max_length=100)),
            ],
            options={
                'verbose_name': 'Employee Status',
                'verbose_name_plural': 'Employee Statuses',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nombre del estado civil', max_length=100)),
            ],
            options={
                'verbose_name': 'Marital Status',
                'verbose_name_plural': 'Marital Statuses',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nombre del municipio', max_length=100)),
            ],
            options={
                'verbose_name': 'Municipality',
                'verbose_name_plural': 'Municipalities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WeklyLoan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Monto pedido (-) o pagado (+)', max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Fecha de registro')),
                ('employee', models.ForeignKey(help_text='Empleado', on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
            options={
                'verbose_name': 'Wekly Loan',
                'verbose_name_plural': 'Wekly Loans',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='marital_status',
            field=models.ForeignKey(help_text='Estado civil', on_delete=django.db.models.deletion.PROTECT, to='employees.maritalstatus'),
        ),
        migrations.AddField(
            model_name='employee',
            name='municipality',
            field=models.ForeignKey(help_text='Municipio', on_delete=django.db.models.deletion.PROTECT, to='employees.municipality'),
        ),
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.ForeignKey(help_text='Estatus', on_delete=django.db.models.deletion.PROTECT, to='employees.employeestatus'),
        ),
    ]
