from django.db import models
from django.contrib.auth.models import User
import uuid


def get_uuid4():
    return str(uuid.uuid4())

class  Vehicle(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', primary_key=True)
	vin = models.CharField(max_length=17, verbose_name="VIN", null=True, blank=True)
	car_number = models.CharField(max_length = 15, verbose_name = 'Гос номер', null=True, blank=True)
	logist = models.ForeignKey(User, verbose_name='Логист', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)

	def __str__(self):

		return '{}'.format(self.car_number)

	def save(self, *args, **kwargs):

		if not self.uid:
			self.uid = get_uuid4()

		super(Vehicle, self).save(*args, **kwargs)


	class Meta:
		verbose_name = 'Автомобиль'
		verbose_name_plural = 'Автомобили'	


class  Driver(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', primary_key=True)
	first_name		= models.CharField(max_length = 30, verbose_name = 'Имя', null=True, blank=True)
	second_name		= models.CharField(max_length = 30, verbose_name = 'Фамилия', null=True, blank=True)
	third_name		= models.CharField(max_length = 30, verbose_name = 'Отчество', null=True, blank=True)

	def __str__(self):

		return '{0} {1}'.format(self.first_name, self.second_name)

	def save(self, *args, **kwargs):

		if not self.uid:
			self.uid = get_uuid4()

		super(Driver, self).save(*args, **kwargs)	

	class Meta:
		verbose_name = 'Водитель'
		verbose_name_plural = 'Водители'



class Route(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', primary_key=True)
	from_date = models.DateField('Дата С', auto_now_add = False, blank=True, null=True)
	to_date = models.DateField('Дата По', auto_now_add = False, blank=True, null=True)
	a_point = models.CharField(max_length = 30, verbose_name = 'Точка А', null=True, blank=True)
	b_point = models.CharField(max_length = 30, verbose_name = 'Точка В', null=True, blank=True)
	route_length = models.DecimalField(verbose_name = 'Протяженность маршрута', max_digits=15, decimal_places=2, blank=True, null=True)
	route_cost = models.DecimalField(verbose_name = 'Стоимость маршрута', max_digits=15, decimal_places=2, blank=True, null=True)
	expenses_1 = models.DecimalField(verbose_name = 'Затрата 1', max_digits=15, decimal_places=2, blank=True, null=True)
	expenses_2 = models.DecimalField(verbose_name = 'Затрата 2', max_digits=15, decimal_places=2, blank=True, null=True)
	expenses_3 = models.DecimalField(verbose_name = 'Затрата 3', max_digits=15, decimal_places=2, blank=True, null=True)
	vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	logist = models.ForeignKey(User, verbose_name='Логист', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	
	def __str__(self):

		return '{}'.format(self.uid)

	def save(self, *args, **kwargs):

		if not self.uid:
			self.uid = get_uuid4()

		super(Route, self).save(*args, **kwargs)	

	class Meta:
		verbose_name = 'Маршрут'
		verbose_name_plural = 'Мартшруты'