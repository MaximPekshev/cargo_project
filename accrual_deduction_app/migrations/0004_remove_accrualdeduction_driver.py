# Generated by Django 3.2.9 on 2022-03-14 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accrual_deduction_app', '0003_alter_accrualdeduction_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accrualdeduction',
            name='driver',
        ),
    ]
