# Generated by Django 3.2.9 on 2021-11-26 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='nds',
            field=models.CharField(blank=True, choices=[('TP', '20%'), ('NO', 'Без НДС')], max_length=2, null=True, verbose_name='Ставка НДС'),
        ),
        migrations.AlterField(
            model_name='route',
            name='client',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cargoapp.organization', verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='route',
            name='depth',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=15, null=True, verbose_name='Глубина, см'),
        ),
        migrations.AlterField(
            model_name='route',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=15, null=True, verbose_name='Высота, см'),
        ),
        migrations.AlterField(
            model_name='route',
            name='volume',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Объем, м3'),
        ),
        migrations.AlterField(
            model_name='route',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Вес, кг'),
        ),
        migrations.AlterField(
            model_name='route',
            name='width',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=15, null=True, verbose_name='Ширина, см'),
        ),
    ]
