# Generated by Django 3.2.9 on 2021-12-15 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0015_alter_dailyindicators_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyindicators',
            name='driver',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cargoapp.driver', verbose_name='Ссылка на водителя'),
        ),
    ]