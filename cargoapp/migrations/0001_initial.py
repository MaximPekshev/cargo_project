# Generated by Django 3.2.6 on 2021-08-23 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.SlugField(blank=True, max_length=36, null=True, verbose_name='Идентификатор')),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=30, null=True, verbose_name='Фамилия')),
                ('third_name', models.CharField(max_length=30, null=True, verbose_name='Отчество')),
            ],
            options={
                'verbose_name': 'Водитель',
                'verbose_name_plural': 'Водители',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.SlugField(blank=True, max_length=36, null=True, verbose_name='Идентификатор')),
                ('vin', models.CharField(max_length=17, null=True, verbose_name='VIN')),
                ('car_number', models.CharField(max_length=15, null=True, verbose_name='Гос номер')),
                ('logist', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Логист')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
    ]
