from django.db import models
from cargoapp.models import Vehicle
from django.conf import settings
import uuid


def get_uuid4():
    return str(uuid.uuid4())

TYPE = (
	( '1' , 'Начисление'),
	( '0' , 'Вычет'),
	)

class ReasonOfDeduction(models.Model):

    title = models.CharField(max_length=25, verbose_name='Наименование')

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Причина начисления/вычета'
        verbose_name_plural = 'Причины начисления/вычета'

class AccrualDeduction(models.Model):

    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    date = models.DateField(verbose_name='Дата')
    vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.CASCADE)
    logist = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Логист', on_delete=models.CASCADE)
    sum = models.DecimalField(verbose_name = 'Сумма', max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    reason = models.ForeignKey(ReasonOfDeduction, verbose_name='Причина начисления/вычета', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, verbose_name='Тип начисления/вычета', choices=TYPE)

    def __str__(self):
        return '{}'.format(self.uid)

    def save(self, *args, **kwargs):

        if not self.uid:
            self.uid = get_uuid4()
            
        super(AccrualDeduction, self).save(*args, **kwargs)     

    class Meta:
        verbose_name = 'Начисление/Вычет'
        verbose_name_plural = 'Начисления/Вычеты'

