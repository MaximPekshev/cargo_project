# Generated by Django 3.2.9 on 2021-12-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0003_auto_20211129_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_contragent',
            field=models.BooleanField(default=False, verbose_name='Контрагент'),
        ),
    ]