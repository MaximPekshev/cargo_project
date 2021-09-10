from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser

from decimal import Decimal

import uuid
from cargoapp.core import upload_route
from django.conf import settings
import datetime
from django.utils.timezone import now

from django.contrib.auth.hashers import make_password
from django.conf import settings

def get_uuid4():
    return str(uuid.uuid4())

class LogistUser(AbstractUser):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	psw = models.CharField(max_length = 25, verbose_name = 'ПСВ', null=True, blank=True, default='')

	def __str__(self):
		return '{}'.format(self.uid)

	def save(self, *args, **kwargs):

		if self.psw:
			self.set_password(self.psw)
			self.psw = ''

		super(LogistUser, self).save(*args, **kwargs)

	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name = 'Логист'
		verbose_name_plural = 'Логисты'


class  Driver(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	title = models.CharField(max_length = 60, verbose_name = 'Наименование', null=True, blank=True, default='')

	first_name		= models.CharField(max_length = 30, verbose_name = 'Имя', null=True, blank=True)
	second_name		= models.CharField(max_length = 30, verbose_name = 'Фамилия', null=True, blank=True)
	third_name		= models.CharField(max_length = 30, verbose_name = 'Отчество', null=True, blank=True)

	def __str__(self):

		return '{0}'.format(self.uid)

	def save(self, *args, **kwargs):

		super(Driver, self).save(*args, **kwargs)	

	class Meta:
		verbose_name = 'Водитель'
		verbose_name_plural = 'Водители'


class  Vehicle(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	vin = models.CharField(max_length=20, verbose_name="VIN", null=True, blank=True)
	car_number = models.CharField(max_length = 15, verbose_name = 'Гос номер', null=True, blank=True)
	logist = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Логист', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	
	def __str__(self):

		return '{}'.format(self.uid)

	def save(self, *args, **kwargs):

		super(Vehicle, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Автомобиль'
		verbose_name_plural = 'Автомобили'
		

class Route(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	from_date = models.DateField('Дата С', auto_now_add = False, blank=True, null=True, default=now)
	to_date = models.DateField('Дата По', auto_now_add = False, blank=True, null=True,  default=now)
	a_point = models.CharField(max_length = 30, verbose_name = 'Точка А', null=True, blank=True)
	b_point = models.CharField(max_length = 30, verbose_name = 'Точка В', null=True, blank=True)
	route_length = models.DecimalField(verbose_name = 'Протяженность маршрута', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	route_cost = models.DecimalField(verbose_name = 'Стоимость маршрута', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	expenses_1 = models.DecimalField(verbose_name = 'Прочие расходы', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	expenses_2 = models.DecimalField(verbose_name = 'Затрата 2', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	expenses_3 = models.DecimalField(verbose_name = 'Затрата 3', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	logist = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Логист', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
	
	def __str__(self):

		return '{}'.format(self.uid)

	def save(self, *args, **kwargs):

		if not self.uid:
			self.uid = get_uuid4()

		super(Route, self).save(*args, **kwargs)

		upload_route(self)

	def get_vehicle(self):

		return '{}'.format(self.vehicle) if self.vehicle else 0

	def get_driver(self):

		return '{}'.format(self.driver) if self.driver else 0

	def get_logist(self):

		return '{}'.format(self.logist) if self.logist else 0

	def get_fuel_cost(self):
		
		return (32*self.route_length/100)*45

	def get_pay_check(self):
		
		return (6*self.route_length)

	def get_pure_income(self):
		
		return (self.route_cost - self.get_fuel_cost() - self.get_pay_check() - self.expenses_1)	

	def get_cost_of_km(self):
		if self.route_length:
			return (self.route_cost/self.route_length).quantize(Decimal("1.00"))
		else:
			return Decimal(0).quantize(Decimal("1.00"))

	def get_cost_of_platon(self):
		
		return (self.route_length*Decimal(1.6)).quantize(Decimal("1.00"))	

	def get_day_count(self):

		if self.to_date and self.from_date:
			return self.to_date-self.from_date
		else:
			return 0

	class Meta:
		verbose_name = 'Маршрут'
		verbose_name_plural = 'Мартшруты'
