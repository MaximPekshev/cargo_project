# Generated by Django 3.2.9 on 2022-04-22 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0028_constant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 4, 22, 10, 31, 51, 595033), null=True, verbose_name='Дата'),
        ),
    ]