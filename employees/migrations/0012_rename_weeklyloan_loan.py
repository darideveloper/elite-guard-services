# Generated by Django 4.2.7 on 2024-12-18 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_employee_photo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeeklyLoan',
            new_name='Loan',
        ),
    ]
