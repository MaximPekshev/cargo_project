# Generated by Django 3.2.9 on 2022-03-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0025_mileagerevenuestandard_net_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='mileagerevenuestandard',
            name='price_of_km',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Норматив цена за километр'),
        ),
    ]