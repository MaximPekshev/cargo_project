# Generated by Django 3.2.9 on 2022-07-15 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_repair_app', '0013_auto_20220715_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalservicework',
            name='from_date_logist',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата начала работ(Логист)'),
        ),
        migrations.AlterField(
            model_name='servicework',
            name='from_date_logist',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата начала работ(Логист)'),
        ),
    ]
