# Generated by Django 3.2.6 on 2022-02-16 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0023_auto_20220214_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='straight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Чистый доход - прямые'),
        ),
    ]
