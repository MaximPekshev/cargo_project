# Generated by Django 3.2.6 on 2021-09-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0004_auto_20210917_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='cost_of_km',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Цена за километр'),
        ),
        migrations.AddField(
            model_name='route',
            name='cost_of_platon',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Платон'),
        ),
        migrations.AddField(
            model_name='route',
            name='day_count',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Количество дней'),
        ),
        migrations.AddField(
            model_name='route',
            name='fuel_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Стоимость топлива'),
        ),
        migrations.AddField(
            model_name='route',
            name='pay_check',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Зарплата'),
        ),
        migrations.AddField(
            model_name='route',
            name='pure_income',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Чистый доход'),
        ),
    ]