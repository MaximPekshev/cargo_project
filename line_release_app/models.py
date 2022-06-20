from django.db import models
from cargoapp.models import Vehicle, Driver, Trailer
from simple_history.models import HistoricalRecords
from cargoapp.models import get_uuid4
import datetime
import calendar


class  LineRelease(models.Model):
    
    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    release_date = models.DateTimeField('Дата выпуска', auto_now_add = True)
    begin_date = models.DateTimeField('Дата начала работы', auto_now_add = False, blank=True, null=True)
    end_date = models.DateTimeField('Дата окончания работы', auto_now_add = False, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    trailer = models.ForeignKey(Trailer, verbose_name='Полуприцеп', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    driver = models.ForeignKey(Driver, verbose_name='Водитель', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    renewal = models.BooleanField(verbose_name='С продлением', default=False)
    for_repair = models.BooleanField(verbose_name='Ремонтный', default=False)

    history = HistoricalRecords()

    def __str__(self):
        
        return '{0}'.format(self.uid)
        
    def save(self, *args, **kwargs):
        
        if not self.uid:
            self.uid = get_uuid4()

        if not self.end_date:
            now = datetime.datetime.now()
            end_of_month = calendar.monthrange(now.year, now.month)[1]
            self.end_date = now.replace(day=end_of_month, hour=23, minute=59)

        super(LineRelease, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Выпуск на линию'
        verbose_name_plural = 'Выпуски на линию'