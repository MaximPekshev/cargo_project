# Generated by Django 3.2.9 on 2022-07-14 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_repair_app', '0004_auto_20220714_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorganization',
            name='is_contragent',
        ),
    ]
