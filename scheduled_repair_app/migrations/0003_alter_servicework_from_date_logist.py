# Generated by Django 3.2.9 on 2022-07-13 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_repair_app', '0002_servicework_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicework',
            name='from_date_logist',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала работ(Логист)'),
        ),
    ]