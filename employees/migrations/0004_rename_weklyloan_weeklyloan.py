# Generated by Django 4.2.7 on 2024-12-14 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_bank_rename_employeestatus_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeklyLoan',
            new_name='WeeklyLoan',
        ),
    ]
