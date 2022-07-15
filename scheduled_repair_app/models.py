from django.db import models
from cargoapp.models import Vehicle, LogistUser
import uuid
from simple_history.models import HistoricalRecords


def get_uuid4():
    return str(uuid.uuid4())

# модель сервисной работы
class  ServiceWork(models.Model):

    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    date = models.DateTimeField('Дата создания', auto_now_add = True)
    title = models.CharField(max_length=150, verbose_name="Наименование", null=True, blank=True, default='')
    vehicle = models.ForeignKey(Vehicle, verbose_name='Автомобиль', on_delete=models.SET_DEFAULT, default=None)
    comment = models.CharField(max_length = 1024, verbose_name = 'Комментарий', null=True, blank=True, default='')
    from_date = models.DateTimeField('Дата начала работ', auto_now_add = False)
    to_date = models.DateTimeField('Дата окончания работ', auto_now_add = False)
    from_date_logist = models.DateTimeField('Дата начала работ(Логист)', auto_now_add = False, null=True, blank=True)
    type = models.ForeignKey('ServiceWorkType', verbose_name='Тип сервисной работы', on_delete=models.SET_DEFAULT, default=None)
    service_organization = models.ForeignKey('ServiceOrganization', verbose_name = 'СТО', on_delete=models.PROTECT, default=None)
    autor = models.ForeignKey(LogistUser, verbose_name = 'Автор заявки', on_delete=models.PROTECT, null=True, blank=True, default=None)
    status = models.ForeignKey('ServiceWorkStatus', verbose_name = 'Статус заявки', on_delete=models.PROTECT, default=None)
    
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        
        if not self.title:

            self.title = self.type.title + ' ' + self.vehicle.car_number

        if not self.uid:

            self.uid = get_uuid4()
        
        super(ServiceWork, self).save(*args, **kwargs)
    
    def get_month_num(self):

        return self.from_date.strftime('%m')

    class Meta:
        verbose_name = 'Сервисная работа'
        verbose_name_plural = 'Сервисные работы'

# типы сервисных работ
class ServiceWorkType(models.Model):

    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    title = models.CharField(max_length = 60, verbose_name = 'Наименование', null=True, blank=True, default='')


    def __str__(self):
        
        return '{0}'.format(self.title)
        
    def save(self, *args, **kwargs):
        
        if not self.uid:
            
            self.uid = get_uuid4()

        super(ServiceWorkType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тип сервисной работы'
        verbose_name_plural = 'Типы сервисной работы'


# модель СТО
class ServiceOrganization(models.Model):
    
    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    title = models.CharField(max_length = 50, verbose_name = 'Наименование', null=True, blank=True)
    full_title = models.CharField(max_length = 128, verbose_name = 'Наименование полное', null=True, blank=True)
    inn = models.CharField(max_length = 12, verbose_name = 'ИНН', null=True, blank=True)
    kpp = models.CharField(max_length = 10, verbose_name = 'КПП', null=True, blank=True)
    ogrn = models.CharField(max_length = 14, verbose_name = 'ОГРН', null=True, blank=True)

    address = models.CharField(max_length = 1024, verbose_name = 'Юридический адрес', null=True, blank=True)
    bank_account = models.CharField(max_length = 20, verbose_name = 'Номер счета', null=True, blank=True)
    bank_bik = models.CharField(max_length = 9, verbose_name = 'БИК банка', null=True, blank=True)
    bank_corr = models.CharField(max_length = 20, verbose_name = 'Корр счет банка', null=True, blank=True)
    bank_title = models.CharField(max_length = 128, verbose_name = 'Наименование банка', null=True, blank=True)
    lon = models.DecimalField(verbose_name = 'Широта', max_digits=10, decimal_places=4, blank=True, null=True, default=0)
    lat = models.DecimalField(verbose_name = 'Широта', max_digits=10, decimal_places=4, blank=True, null=True, default=0)
    
    def __str__(self):
        
        return '{}'.format(self.title)
        
    def save(self, *args, **kwargs):

        if not self.uid:
            
            self.uid = get_uuid4()
        
        super(ServiceOrganization, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Сервисная организация'
        verbose_name_plural = 'Сервисные организации'

# статус сервисных работ
class ServiceWorkStatus(models.Model):

    uid = models.SlugField(max_length=36, verbose_name='Идентификатор', unique=True)
    title = models.CharField(max_length = 60, verbose_name = 'Наименование', null=True, blank=True, default='')

    def __str__(self):
        
        return '{0}'.format(self.title)
        
    def save(self, *args, **kwargs):
        
        if not self.uid:
            
            self.uid = get_uuid4()

        super(ServiceWorkStatus, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статус сервисной работы'
        verbose_name_plural = 'Статусы сервисных работ'
