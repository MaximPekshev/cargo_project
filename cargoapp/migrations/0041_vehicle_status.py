# Generated by Django 3.2.9 on 2022-07-07 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0040_vehicle_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cargoapp.vehicle_status', verbose_name='Статус'),
        ),
    ]