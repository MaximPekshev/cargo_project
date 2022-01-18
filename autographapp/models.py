from django.db import models
from cargoapp.models import Vehicle, Driver

class AutographDailyIndicators(models.Model):

	date = models.DateField('Дата', auto_now_add = False)
	maxSpeed = models.DecimalField(verbose_name = 'Максимальная скорость', max_digits=10, decimal_places=2, blank=True, null=True)
	averageSpeed = models.DecimalField(verbose_name = 'Средняя скорость', max_digits=10, decimal_places=2, blank=True, null=True)
	fuelConsumPerDay = models.DecimalField(verbose_name = 'Расход по баку в л. за сутки', max_digits=10, decimal_places=2, blank=True, null=True)
	fuelConsumPer100km = models.DecimalField(verbose_name = 'Расход по баку в л. на 100 км', max_digits=10, decimal_places=2, blank=True, null=True)
	rotationMAX = models.DecimalField(verbose_name = 'Обороты макс', max_digits=10, decimal_places=2, blank=True, null=True)
	parkCount = models.PositiveIntegerField(verbose_name = 'Количество остановок', blank=True, null=True)
	parkCount5MinMore = models.PositiveIntegerField(verbose_name = 'Количество остановок с вкл. ДВС более 5 минут', blank=True, null=True)
	hardBrakingCount = models.PositiveIntegerField(verbose_name = 'Количество резких торможений', blank=True, null=True)
	totalDistance = models.DecimalField(verbose_name = 'Суточный пробег', max_digits=10, decimal_places=2, blank=True, null=True)
	vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.PROTECT, blank=True, null=True, default=None)
	driver = models.ForeignKey(Driver, verbose_name = 'Водитель', on_delete=models.PROTECT, blank=True, null=True, default=None)

	def __str__(self):
		return '{}'.format(self.pk)

	def save(self, *args, **kwargs):

		super(AutographDailyIndicators, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Дневные показатели автографа'
		verbose_name_plural = 'Дневные показатели автографа'
