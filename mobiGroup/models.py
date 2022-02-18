from django.db import models

class Query(models.Model):
    query = models.TextField(verbose_name='Вопрос',max_length=4000)
    answer1 = models.CharField(verbose_name='Ответ 1', max_length=250)
    answer2 = models.CharField(verbose_name='Ответ 2', max_length=250)
    answer3 = models.CharField(verbose_name='Ответ 3 (не обязательно)', null=True, blank=True, max_length=250)
    answer4 = models.CharField(verbose_name='Ответ 4 (не обязательно)', null=True, blank=True, max_length=250)
    answer5 = models.CharField(verbose_name='Ответ 5 (не обязательно)', null=True, blank=True, max_length=250)
    answer6 = models.CharField(verbose_name='Ответ 6 (не обязательно)', null=True, blank=True, max_length=250)
    answer7 = models.CharField(verbose_name='Ответ 7 (не обязательно)', null=True, blank=True, max_length=250)
    correctAnswer = models.IntegerField(verbose_name='Правильный ответ')
    explanation = models.TextField(verbose_name='объяснение',max_length=2000,null=True, blank=True,)
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        
    def __str__(self):
        return self.query
    
class Test(models.Model):
    token = models.CharField(verbose_name='Токен',help_text="Неповторимий элемент", max_length=100)
    fio = models.CharField(verbose_name='Водитель', max_length=100)
    number = models.CharField(verbose_name='Номер телефона', max_length=100)
    columnar = models.CharField(verbose_name='Kолонный', max_length=100)
    carNumber = models.CharField(verbose_name='Гос номер', max_length=100)
    carModel = models.CharField(verbose_name='Модель транспортного средства', max_length=100)
    successfully = models.BooleanField(verbose_name='Пройдено',blank=True)
    date = models.DateField(verbose_name='Дата', auto_now=True,)
    selectedAnswers = models.CharField(verbose_name='Выбранные ответы', max_length=250,help_text="ИД вопроса(1):Ответ, ИД вопроса(2):Ответ, ... ,ИД вопроса(N):Ответ")
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        
    def __str__(self):
        if self.successfully:
            return  '✅ Пройденно, '+ self.fio[:20] + ' ' + self.number[:20] +' '+ str(self.date) 
        return  '❌ Не пройденно, '+ self.fio[:20] + ' ' + self.number[:20] +' '+ str(self.date) 
    