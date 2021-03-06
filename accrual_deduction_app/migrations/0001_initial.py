# Generated by Django 3.2.9 on 2022-03-11 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cargoapp', '0026_mileagerevenuestandard_price_of_km'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReasonOfDeduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Причина начисления/вычета',
                'verbose_name_plural': 'Причины начисления/вычета',
            },
        ),
        migrations.CreateModel(
            name='AccrualDeduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.SlugField(max_length=36, unique=True, verbose_name='Идентификатор')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sum', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Сумма')),
                ('type', models.CharField(choices=[(1, 'Начисление'), (0, 'Вычет')], max_length=1, verbose_name='Тип начисления/вычета')),
                ('logist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Логист')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accrual_deduction_app.reasonofdeduction', verbose_name='Причина начисления/вычета')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargoapp.vehicle', verbose_name='Автомобиль')),
            ],
        ),
    ]
