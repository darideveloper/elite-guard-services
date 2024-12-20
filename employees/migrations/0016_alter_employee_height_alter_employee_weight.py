# Generated by Django 4.2.7 on 2024-12-18 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_rename_colony_neighborhood_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Estatura en metros', max_digits=3, verbose_name='Estatura'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Peso en kilogramos', max_digits=5, verbose_name='Peso'),
            preserve_default=False,
        ),
    ]
