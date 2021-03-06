# Generated by Django 3.2.9 on 2022-07-14 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cargoapp', '0042_auto_20220707_1256'),
        ('scheduled_repair_app', '0005_remove_serviceorganization_is_contragent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceWorkStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.SlugField(max_length=36, unique=True, verbose_name='Идентификатор')),
                ('title', models.CharField(blank=True, default='', max_length=60, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Статус сервисной работы',
                'verbose_name_plural': 'Статусы сервисных работ',
            },
        ),
        migrations.CreateModel(
            name='HistoricalServiceWork',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.SlugField(max_length=36, verbose_name='Идентификатор')),
                ('title', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Наименование')),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Комментарий')),
                ('from_date', models.DateField(verbose_name='Дата начала работ')),
                ('to_date', models.DateField(verbose_name='Дата окончания работ')),
                ('from_date_logist', models.DateField(blank=True, null=True, verbose_name='Дата начала работ(Логист)')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('service_organization', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='scheduled_repair_app.serviceorganization', verbose_name='СТО')),
                ('type', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='scheduled_repair_app.serviceworktype', verbose_name='Тип сервисной работы')),
                ('vehicle', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cargoapp.vehicle', verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'historical Сервисная работа',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
