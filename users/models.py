from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from catalog.models import JobTitle, Receiver, Podrazd, Sotr

class CustomUser(AbstractUser):

    JT = models.ForeignKey(JobTitle,on_delete=models.CASCADE, null=True, verbose_name='Должность')
    OBJ = models.ForeignKey(Receiver,on_delete=models.CASCADE, null=True, verbose_name='Объект производства')
    POD = models.ForeignKey(Podrazd,on_delete=models.CASCADE, null=True, verbose_name='Подразделение')
    TEL = models.CharField(max_length=30, verbose_name='Телефон', default='', null=True, blank=True) #Телефон
    TELEGRAMID = models.CharField(max_length=30, verbose_name='Telegram ID', default='', null=True, blank=True) #Телеграм ID

    A_Tabel = models.BooleanField(default=False, null=True, 
                                verbose_name='Ввод табеля', blank=True) # разрешение на ввод табеля
    A_TabelAdmin = models.BooleanField(default=False, null=True, 
                 verbose_name='Ввод табеля Админ', blank=True) # разрешение на ввод табеля Админский

    A_TabelReport = models.BooleanField(default=False, null=True, 
                 verbose_name='Отчет по табелю', blank=True)            # разрешение отчет по табелю
    
    A_TabelReportAdmin = models.BooleanField(default=False, null=True, 
                 verbose_name='Отчет по табелю Админ', blank=True)      # разрешение отчет по табелю Админ

    A_Den = models.BooleanField(default=False, null=True, 
                 verbose_name='Ввод рабочего дня', blank=True)      # разрешение на ввод рабочего дня

    A_DenReport = models.BooleanField(default=False, null=True, 
                 verbose_name='Отчет по рабочим дням', blank=True)      # разрешение на отчет по рабочим дням

    A_Graphic = models.BooleanField(default=False, null=True, 
                 verbose_name='Ведение графика', blank=True)      # разрешение на ведение графика

    A_Banket = models.BooleanField(default=False, null=True, 
                 verbose_name='Просмотр раздела банкеты', blank=True)      # разрешение на просмотр банкетов

    A_BanketFin = models.BooleanField(default=False, null=True, 
                 verbose_name='Просмотр фин.инф. банкетов', blank=True)      # разрешение на просмотр финансовой информации банкетов

    A_BanketEdit = models.BooleanField(default=False, null=True, 
                 verbose_name='Созд/Изм/Удал. банкетов', blank=True)      # разрешение на создание/изменение/удаление банкетов
        
    sotr = models.ForeignKey(Sotr,on_delete=models.CASCADE, null=True, verbose_name='Сотрудник', blank=True)

