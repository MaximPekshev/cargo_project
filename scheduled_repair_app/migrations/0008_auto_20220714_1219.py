# Generated by Django 3.2.9 on 2022-07-14 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_repair_app', '0007_auto_20220714_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalservicework',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='servicework',
            name='autor',
        ),
    ]
