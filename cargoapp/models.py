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

NDS_RATE = (
	('TP', '20%'),
	('NO', 'Без НДС'),
	)


def get_uuid4():
    return str(uuid.uuid4())

def get_image_name(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.uid
	return new_name


class LogistUser(AbstractUser):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	psw = models.CharField(max_length = 25, verbose_name = 'ПСВ', null=True, blank=True, default='')

	def __str__(self):
		return '{}'.format(self.username)

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

		return '{0}'.format(self.title)

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

		return '{}'.format(self.car_number)

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
	
	fuel_cost = models.DecimalField(verbose_name = 'Стоимость топлива', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	pay_check = models.DecimalField(verbose_name = 'Зарплата', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	pure_income = models.DecimalField(verbose_name = 'Чистый доход', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	cost_of_km = models.DecimalField(verbose_name = 'Цена за километр', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	cost_of_platon = models.DecimalField(verbose_name = 'Платон', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	day_count = models.DecimalField(verbose_name = 'Количество дней', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
	
	organization = models.ForeignKey('Organization', verbose_name = 'Организация', on_delete=models.SET_DEFAULT, related_name='route_organization', default=None, null=True, blank=True)
	contragent = models.ForeignKey('Organization', verbose_name = 'Контрагент', on_delete=models.SET_DEFAULT, related_name='route_contragent', default=None, null=True, blank=True)
	contract = models.ForeignKey('Contracts', verbose_name = 'Договор', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

	request_img	= models.ImageField(upload_to=get_image_name, verbose_name='Скан Заявки', null=True, blank=True, default=None)
	loa_img	= models.ImageField(upload_to=get_image_name, verbose_name='Скан доверенности', null=True, blank=True, default=None)
	weight = models.DecimalField(verbose_name='Вес, т', max_digits=15, decimal_places=2, null=True, blank=True, default=0)
	request_number = models.CharField(max_length = 30, verbose_name = 'Номер заявки', null=True, blank=True, default='')

	banner_all = models.BooleanField(verbose_name='Растентовка полная', default=False)
	banner_side = models.BooleanField(verbose_name='Растентовка бок', default=False)
	control_penalty = models.BooleanField(verbose_name='Штраф контроля', default=False)

	cargo_description = models.CharField(max_length = 256, verbose_name = 'Описание груза', null=True, blank=True, default='')


	def __str__(self):

		return '{}'.format(self.uid)

	def save(self, *args, **kwargs):

		if not self.uid:
			self.uid = get_uuid4()

		self.fuel_cost = 32*self.route_length/100*45
		self.pay_check = 6*self.route_length
		self.pure_income = self.route_cost - self.fuel_cost - self.pay_check - self.expenses_1
		if self.route_length:
			self.cost_of_km = self.route_cost/self.route_length
		else:
			self.cost_of_km = 0
		self.cost_of_platon = self.route_length*Decimal(1.6)
		if self.to_date and self.from_date:
			self.day_count = (self.to_date-self.from_date).days
		else:
			self.day_count = 0

		super(Route, self).save(*args, **kwargs)

		upload_route(self)

	def get_client(self):

		return '{}'.format(self.organization.uid) if self.organization else 0

	def get_vehicle(self):

		return '{}'.format(self.vehicle.uid) if self.vehicle else 0

	def get_driver(self):

		return '{}'.format(self.driver.uid) if self.driver else 0

	def get_logist(self):

		return '{}'.format(self.logist.uid) if self.logist else 0

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


class City(models.Model):

	code = models.CharField(max_length = 25, verbose_name = 'Код КЛАДР', unique=True)
	title = models.CharField(max_length = 30, verbose_name = 'Наименование', null=True, blank=True, default='')
	reduction = models.CharField(max_length = 5, verbose_name = 'Сокращение', null=True, blank=True, default='')

	def __str__(self):
		return '{}'.format(self.title)

	class Meta:
		verbose_name = 'Город'
		verbose_name_plural = 'Города'


class Organization(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	title = models.CharField(max_length = 50, verbose_name = 'Наименование', null=True, blank=True)
	full_title = models.CharField(max_length = 128, verbose_name = 'Наименование полное', null=True, blank=True)
	inn = models.CharField(max_length = 12, verbose_name = 'ИНН', null=True, blank=True)
	kpp = models.CharField(max_length = 10, verbose_name = 'КПП', null=True, blank=True)
	ogrn = models.CharField(max_length = 14, verbose_name = 'ОГРН', null=True, blank=True)

	is_contragent = models.BooleanField(verbose_name='Контрагент', default=False)
	
	address = models.CharField(max_length = 1024, verbose_name = 'Юридический адрес', null=True, blank=True)
	nds = models.CharField(max_length=2, verbose_name='Ставка НДС', choices=NDS_RATE, null=True, blank=True)

	bank_account = models.CharField(max_length = 20, verbose_name = 'Номер счета', null=True, blank=True)
	bank_bik = models.CharField(max_length = 9, verbose_name = 'БИК банка', null=True, blank=True)
	bank_corr = models.CharField(max_length = 20, verbose_name = 'Корр счет банка', null=True, blank=True)
	bank_title = models.CharField(max_length = 128, verbose_name = 'Наименование банка', null=True, blank=True)


	def __str__(self):
		return '{}'.format(self.title)

	def save(self, *args, **kwargs):

		super(Organization, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Организация'
		verbose_name_plural = 'Организации'

class Contracts(models.Model):

	uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
	title = models.CharField(max_length = 100, verbose_name = 'Наименование', null=True, blank=True)
	number = models.CharField(max_length = 50, verbose_name = 'Номер', null=True, blank=True)
	date = models.DateField('Дата', auto_now_add = False)

	organization = models.ForeignKey(Organization, verbose_name = 'Организация', on_delete=models.PROTECT, related_name='organization', null=True, blank=True)
	contragent = models.ForeignKey(Organization, verbose_name = 'Контрагент', on_delete=models.PROTECT, related_name='contragent', null=True, blank=True)


	def __str__(self):
		return '{}'.format(self.title)

	def save(self, *args, **kwargs):

		super(Contracts, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Договор'
		verbose_name_plural = 'Договоры'