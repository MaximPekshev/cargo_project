# Generated by Django 3.2.9 on 2022-07-13 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduled_repair_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicework',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='scheduled_repair_app.serviceworktype', verbose_name='Тип сервисной работы'),
        ),
    ]
