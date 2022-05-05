from django.db import models
from select import select
from django.utils.timezone import now

from cargoapp.models import Vehicle, Trailer

INSURANCE_TYPE = (
	('0', 'ОСАГО'),
	('1', 'КАСКО'),
	)

class VehicleInsurance(models.Model):

    vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, verbose_name='Тип страховки', choices=INSURANCE_TYPE)
    from_date = models.DateField('Дата С', auto_now_add = False, blank=True, null=True, default=now)
    to_date = models.DateField('Дата По', auto_now_add = False, blank=True, null=True,  default=now)
    contragent = models.ForeignKey('ContragentInsurance', verbose_name = 'Страховая компания', on_delete=models.PROTECT, default=None, null=True, blank=True)
    owner = models.ForeignKey('OwnerInsurance', verbose_name = 'Собственник', on_delete=models.PROTECT, default=None, null=True, blank=True)

    def __str__(self):

        return '{}'.format(self.id)

    class Meta:
        verbose_name = 'Страховка автомобиля'
        verbose_name_plural = 'Страховки автомобилей'

class TrailerInsurance(models.Model):

    trailer = models.ForeignKey(Trailer, verbose_name='Полуприцеп', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, verbose_name='Тип страховки', choices=INSURANCE_TYPE)
    from_date = models.DateField('Дата С', auto_now_add = False, blank=True, null=True, default=now)
    to_date = models.DateField('Дата По', auto_now_add = False, blank=True, null=True,  default=now)
    contragent = models.ForeignKey('ContragentInsurance', verbose_name = 'Страховая компания', on_delete=models.PROTECT, default=None, null=True, blank=True)
    owner = models.ForeignKey('OwnerInsurance', verbose_name = 'Собственник', on_delete=models.PROTECT, default=None, null=True, blank=True)

    def __str__(self):

        return '{}'.format(self.id)

    class Meta:
        verbose_name = 'Страховка полуприцепа'
        verbose_name_plural = 'Страховки полуприцепов'        


class ContragentInsurance(models.Model):

    title = models.CharField(max_length = 50, verbose_name = 'Наименование')


    def __str__(self):

        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Страховая компания'
        verbose_name_plural = 'Страховые компании'

class OwnerInsurance(models.Model):

    title = models.CharField(max_length = 50, verbose_name = 'Наименование')


    def __str__(self):

        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Собственник'
        verbose_name_plural = 'Собственники'        