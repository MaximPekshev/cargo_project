# Generated by Django 3.2.9 on 2022-01-31 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0020_alter_vehicle_nav_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistuser',
            name='supervisor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Руководитель'),
        ),
    ]
