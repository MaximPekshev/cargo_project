# Generated by Django 3.2.9 on 2021-12-02 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0009_auto_20211202_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='client',
            new_name='organization',
        ),
    ]