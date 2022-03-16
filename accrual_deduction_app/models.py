from django.db import models
from cargoapp.models import Vehicle, Driver
from django.conf import settings
import uuid
from .core import upload_accrual


def get_uuid4():
    return str(uuid.uuid4())

TYPE = (
	( '1' , 'Начисление'),
	( '0' , 'Вычет'),
	)

class ReasonOfDeduction(models.Model):

    title = models.CharField(max_length=250, verbose_name='Наименование')

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Причина начисления/вычета'
        verbose_name_plural = 'Причины начисления/вычета'

class AccrualDeduction(models.Model):

    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    date = models.DateField(verbose_name='Дата')
    vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.CASCADE,null=True, blank=True, default=None)
    logist = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Логист', on_delete=models.CASCADE)
    sum = models.DecimalField(verbose_name = 'Сумма', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    reason = models.ForeignKey(ReasonOfDeduction, verbose_name='Причина начисления/вычета', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, verbose_name='Тип начисления/вычета', choices=TYPE)

    comment = models.CharField(max_length = 512, verbose_name = 'Комментарий', null=True, blank=True, default='')
    upload_status = models.BooleanField(verbose_name='Статус выгрузки 1С', default=False)

    def __str__(self):
        return '{}'.format(self.uid)

    def save(self, *args, **kwargs):

        if not self.uid:
            self.uid = get_uuid4()
            
        if not self.driver:
            self.driver = self.vehicle.driver  
            
        super(AccrualDeduction, self).save(*args, **kwargs)
        if not self.upload_status:
            upload_accrual(self)


    def get_vehicle(self):
        return '{}'.format(self.vehicle.uid) if self.vehicle else 0
        
    def get_driver(self):
        return '{}'.format(self.driver.uid) if self.driver else 0
    
    def get_logist(self):
        return '{}'.format(self.logist.uid) if self.logist else 0

    def get_reason(self):
        return '{}'.format(self.reason) if self.logist else 0

    def get_comment(self):
        return '{}'.format(self.comment) if self.logist else 0    

    class Meta:
        verbose_name = 'Начисление/Вычет'
        verbose_name_plural = 'Начисления/Вычеты'

