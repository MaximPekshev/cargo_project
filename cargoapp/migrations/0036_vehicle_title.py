# Generated by Django 3.2.9 on 2022-04-29 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0035_auto_20220428_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='title',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Название'),
        ),
    ]
