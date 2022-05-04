# Generated by Django 3.2.9 on 2022-05-04 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0003_alter_vehicleinsurance_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Собственник',
                'verbose_name_plural': 'Собственники',
            },
        ),
        migrations.AddField(
            model_name='vehicleinsurance',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='insurance_app.ownerinsurance', verbose_name='Собственник'),
        ),
    ]