from django.db import models
#from users.models import CustomUser
#from catalog.models import JobTitle, Receiver, Podrazd, Sotr
#from django.contrib.auth.models import User

# Create your models here.

# Справочник задач
class Task (models.Model):
    taskname = models.CharField('Название задачи', max_length=150)

    def __str__(self) -> str:
        return self.taskname

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Перечень задач'

# Справочник должностей
class JobTitle (models.Model):
    jobtitlename = models.CharField('Название должности', max_length=60, db_index=True)

    def __str__(self) -> str:
        return self.jobtitlename

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'       


# Справочник задач по чек-листу для должности
class TaskJobTitle(models.Model):
    name = models.CharField(max_length=60, verbose_name='Наименование чек-листа')
    jobtitle = models.ForeignKey('JobTitle', on_delete=models.CASCADE, null=True, verbose_name='Должность')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Чек-лист сотрудника'
        verbose_name_plural = 'Чек-листы сотрудников'

class ChekListTask(models.Model):
    ChekList = models.ForeignKey('TaskJobTitle', on_delete=models.PROTECT,null=False)        
    Tasks = models.ManyToManyField('Task')
    Order = models.IntegerField (blank=True, null=True)

class CheckListTaskItem(models.Model):    
    order = models.IntegerField('Порядок')
    cheklistlink = models.ForeignKey('TaskJobTitle', on_delete=models.CASCADE, null=True, verbose_name='Чек-лист')
    tasklink = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, verbose_name='Задача')
    time_control = models.TimeField('Время контроля', null=True, )
 
class TaskExe(models.Model):    # задачи на выполнение для должности
    date = models.DateField(null=True) #дата на выполнение
    tasklink = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, verbose_name='Задача') #ссылка на задачу
    jobtitlelink = models.ForeignKey('JobTitle', on_delete=models.CASCADE, null=True, verbose_name='Должность') #ссылка на должность
    taskjobtitlelink = models.ForeignKey('TaskJobTitle', on_delete=models.CASCADE, null=True, verbose_name='Чек-лист') #ссылка на чек-лист
    time_control = models.TimeField(null=True) #время контроля
    order = models.IntegerField(null=True) #порядок сортировки
    status = models.BooleanField(default=False) #статус выполнен/невыполнен
    user_exe = models.CharField(max_length=60, verbose_name='Пользователь', default='', null=True) #пользователь который выполнил сохраним в строке
    time_exe = models.DateTimeField(null=True, verbose_name='Дата/время исполнения', auto_now=True)

    class Meta:
       verbose_name = ' Задача на выполнение'
       verbose_name_plural = ' Задачи на выполнение'
        
# справочник чек листов
class ChList(models.Model):  
    name = models.CharField(max_length=60, verbose_name='Наименование чек-листа')
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на объект (Марта, EL Gusto)
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на подразделение (Бар, Кухня)
    t1 = models.TimeField(null=True, verbose_name='t Начало', blank=True)
    t2 = models.TimeField(null=True, verbose_name='t Конец', blank=True)
    u1 = models.CharField(null=True, blank=True, max_length=20, verbose_name='Участок 1') # Наименование участка 1
    u2 = models.CharField(null=True, blank=True, max_length=20, verbose_name='Участок 2') # Наименование участка 2
    u3 = models.CharField(null=True, blank=True, max_length=20, verbose_name='Участок 3') # Наименование участка 3
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
       verbose_name = 'Чек лист'
       verbose_name_plural = 'Чек листы'

# справочник записей по чек листам, по которым надо формировать задания
class ChListRec(models.Model):     
 
    order = models.IntegerField(null=True, verbose_name='Порядок', blank=True) # для сортировки
    name = models.CharField(max_length=300, verbose_name='Наименование записи чек-листа')
    chl = models.ForeignKey('ChList', on_delete=models.CASCADE, null=True, verbose_name='Чек-лист') #ссылка на чек лист (у каждого подразделения свой чек лист)
    t1 = models.TimeField(null=True, verbose_name='t Начало', blank=True)
    t2 = models.TimeField(null=True, verbose_name='t Конец', blank=True)
    ct1 = models.TimeField(null=True, verbose_name='t Начало', blank=True) #Время контроля
    ct2 = models.TimeField(null=True, verbose_name='t Конец', blank=True) #Время контроля

    def __str__(self) -> str:
        return self.name

    class Meta:
       verbose_name = 'Чек лист (запись)'
       verbose_name_plural = 'Чек лист (записи)'

# справочник записей с заданиями по чек листам, которые формирутся ежедневно
class ChListTask(models.Model): 

    date = models.DateField(null=True) #дата задания по чек листу
    chl = models.ForeignKey('ChList', on_delete=models.CASCADE, null=True, verbose_name='Чек-лист') #ссылка на чек лист (у каждого подразделения свой чек лист)
    chlrec = models.ForeignKey('ChListRec', on_delete=models.CASCADE, null=True, verbose_name='Чек-лист-запись', related_name="ChList_Record") #ссылка на запись чек листа по которому сформировано это задание
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на объект (Марта, EL Gusto)
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на подразделение (Бар, Кухня)
    created = models.TimeField(null=True, blank=True, auto_now=True) # Время создания записи
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name="tasks_author") # Автор

    f1 = models.BooleanField('f1', default=False, null=True, blank=True)
    t1 = models.DateTimeField('t1', null=True, blank=True) # Время выполнения 1
    s1 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="s1_author", blank=True) # Выполнил сотрудник 1

    f2 = models.BooleanField('f2', default=False, null=True, blank=True)
    t2 = models.DateTimeField('t2', null=True, blank=True) # Время выполнения 2
    s2 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="s2_author", blank=True) # Выполнил сотрудник 2

    f3 = models.BooleanField('f3', default=False, null=True, blank=True)
    t3 = models.DateTimeField('t3', null=True, blank=True) # Время выполнения 3
    s3 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="s3_author", blank=True) # Выполнил сотрудник 3

    cf1 = models.BooleanField('cf1', default=False, null=True, blank=True)
    ct1 = models.DateTimeField('ct1', null=True, blank=True) # Время выполнения 1
    cs1 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="cs1_author", blank=True) # Проверил сотрудник 1

    cf2 = models.BooleanField('cf2', default=False, null=True, blank=True)
    ct2 = models.DateTimeField('ct2', null=True, blank=True) # Время выполнения 2
    cs2 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="cs2_author", blank=True) # Проверил сотрудник 2

    cf3 = models.BooleanField('cf3', default=False, null=True, blank=True)
    ct3 = models.DateTimeField('ct3', null=True, blank=True) # Время выполнения 3
    cs3 = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, related_name="cs3_author", blank=True) # Проверил сотрудник 3

    cst1 = models.BooleanField('cst1', default=True, null=True, blank=True) # Статус контроля, по умолчанию Ок
    cst2 = models.BooleanField('cst2', default=True, null=True, blank=True) # Статус контроля, по умолчанию Ок
    cst3 = models.BooleanField('cst3', default=True, null=True, blank=True) # Статус контроля, по умолчанию Ок

    rem1 = models.CharField(max_length=60, verbose_name='Remark по работе uch1', default='', null=True, blank=True) # Комментарий по работе по участку 1
    rem2 = models.CharField(max_length=60, verbose_name='Remark по работе uch2', default='', null=True, blank=True) # Комментарий по работе по участку 2
    rem3 = models.CharField(max_length=60, verbose_name='Remark по работе uch3', default='', null=True, blank=True) # Комментарий по работе по участку 3

    def __str__(self) -> str:
        return self.chlrec.name

    class Meta:
       verbose_name = 'Запись в чек листе'
       verbose_name_plural = 'Записи в чек листах'

# Справочник источника закупа
class Source (models.Model):
    name = models.CharField('Место закупа', max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Место закупа'
        verbose_name_plural = 'Места закупа'

# Справочник единиц измерения
class Ei (models.Model):
    name = models.CharField('Единица измерения', max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

# Справочник приемника (объектов хранения/производства/место работы)
class Receiver (models.Model):
    name = models.CharField('Оъект', max_length=150)
    img = models.ImageField('Изображение', upload_to='static/IMG', default='', null=True, max_length=200, blank=True)  #изображение
    k = models.IntegerField('Коэффициент', null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объект'

# Справочник номенклатуры
class Nomen (models.Model):
    name = models.CharField('Номенклатура', max_length=150)
    ei = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Ед.') #ссылка на единицу измерения
    img = models.ImageField('Изображение', upload_to='static/IMG', default='', null=True, max_length=200, blank=True)  #изображение
    order = models.IntegerField('Порядок', default=0, null=True)
    cost = models.IntegerField('Цена', default=0, null=True)
    source_link = models.ForeignKey('Source', on_delete=models.CASCADE, null=True, verbose_name='Место закупа') #ссылка на базу откуда закупают
    opisanie = models.TextField('Описание', default='', null=True, max_length=500, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Номенклатуру'
        verbose_name_plural = 'Номенклатура'

# Справочник заявок
class Zakaz (models.Model):

    date = models.DateField(null=True) #дата заявки
    nomen_link = models.ForeignKey('Nomen', on_delete=models.CASCADE, null=True, verbose_name='Номенклатура') #ссылка на номенклатуру
    ei_link = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Ед.') #ссылка на единицу измерения
    kol = models.FloatField('Количество', default=0, null=True)
    cost = models.IntegerField('Цена', default=0, null=True)
    source_link = models.ForeignKey('Source', on_delete=models.CASCADE, null=True, verbose_name='База/Магазин') #ссылка на базу откуда закупают
    receiver_link = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на место куда везут
    creator = models.CharField(max_length=30, verbose_name='Создатель', default='', null=True, blank=True) #пользователь который создал заявку
    time_create = models.DateTimeField(null=True, verbose_name='Дата/время создания', auto_now=True, blank=True)
    maker = models.CharField(max_length=30, verbose_name='Исполнитель', default='', null=True, blank=True) #пользователь который выполнил заказ
    time_make = models.DateTimeField(null=True, verbose_name='Дата/время выполнения', auto_now=False, blank=True)
    deliver = models.CharField(max_length=30, verbose_name='Доставил', default='', null=True, blank=True) #пользователь который доставил заказ
    time_deliv = models.DateTimeField(null=True, verbose_name='Дата/время доставления', auto_now=False, blank=True)
    status = models.IntegerField('Статус', default=0)   # 0 - заявка в работе, 1 - заявка выполнена, 2 - заявка доставлена

    class Meta:
        verbose_name = 'Заявка на закупку'
        verbose_name_plural = 'Заявки на закупку'

# Справочник комментарий к заявке
class Zakazremark (models.Model):
    date = models.DateTimeField(null=True) #дата ремарки
    remark = models.CharField('Комментарий', max_length=200)
    creator = models.CharField(max_length=30, verbose_name='Пользователь', default='', null=True) #пользователь который создал заявку
    time_create = models.DateTimeField(null=True, verbose_name='Дата/время создания', auto_now=True)
    maker = models.CharField(max_length=30, verbose_name='Пользователь', default='', null=True) #пользователь который выполнил заказ
    time_make = models.DateTimeField(null=True, verbose_name='Дата/время выполнения', auto_now=True)
    status = models.BooleanField(default=False) #статус выполнен/невыполнен
    
    def __str__(self) -> str:
        return self.remark

    class Meta:
        verbose_name = 'Коментарий к заявке'
        verbose_name_plural = 'Комментарии к заявке'

# Справочник номенклатуры для химии
class NomenHim (models.Model):
    name = models.CharField('Номенклатура', max_length=150)
    ei = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Ед.') #ссылка на единицу измерения
    img = models.ImageField('Изображение', upload_to='static/IMG', default='', null=True, max_length=200, blank=True)  #изображение
    order = models.IntegerField('Порядок', default=0, null=True)
    cost = models.IntegerField('Цена', default=0, null=True)
    source_link = models.ForeignKey('Source', on_delete=models.CASCADE, null=True, verbose_name='Место закупа') #ссылка на базу откуда закупают
    opisanie = models.TextField('Описание', default='', null=True, max_length=500, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Химия'
        verbose_name_plural = 'Химия'

# Справочник заявок по химии
class ZakazHim (models.Model):

    date = models.DateField(null=True) #дата заявки
    nomen_link = models.ForeignKey('NomenHim', on_delete=models.CASCADE, null=True, verbose_name='Химия') #ссылка на номенклатуру
    ei_link = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Ед.') #ссылка на единицу измерения
    kol = models.FloatField('Количество', default=0, null=True)
    cost = models.IntegerField('Цена', default=0, null=True)
    source_link = models.ForeignKey('Source', on_delete=models.CASCADE, null=True, verbose_name='База/Магазин') #ссылка на базу откуда закупают
    receiver_link = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на место куда везут
    creator = models.CharField(max_length=30, verbose_name='Создатель', default='', null=True, blank=True) #пользователь который создал заявку
    time_create = models.DateTimeField(null=True, verbose_name='Дата/время создания', auto_now=True, blank=True)
    maker = models.CharField(max_length=30, verbose_name='Исполнитель', default='', null=True, blank=True) #пользователь который выполнил заказ
    time_make = models.DateTimeField(null=True, verbose_name='Дата/время выполнения', auto_now=False, blank=True)
    deliver = models.CharField(max_length=30, verbose_name='Доставил', default='', null=True, blank=True) #пользователь который доставил заказ
    time_deliv = models.DateTimeField(null=True, verbose_name='Дата/время доставления', auto_now=False, blank=True)
    status = models.IntegerField('Статус', default=0)   # 0 - заявка в работе, 1 - заявка выполнена, 2 - заявка доставлена

    class Meta:
        verbose_name = 'Заявка на химию'
        verbose_name_plural = 'Заявки на химию'

# Справочник комментарий к заявке на химию
class ZakazremarkHim (models.Model):
    date = models.DateTimeField(null=True) #дата ремарки
    remark = models.CharField('Комментарий', max_length=200)
    creator = models.CharField(max_length=30, verbose_name='Пользователь', default='', null=True) #пользователь который создал заявку
    time_create = models.DateTimeField(null=True, verbose_name='Дата/время создания', auto_now=True)
    maker = models.CharField(max_length=30, verbose_name='Пользователь', default='', null=True) #пользователь который выполнил заказ
    time_make = models.DateTimeField(null=True, verbose_name='Дата/время выполнения', auto_now=True)
    status = models.BooleanField(default=False) #статус выполнен/невыполнен
    
    def __str__(self) -> str:
        return self.remark

    class Meta:
        verbose_name = 'Коментарий к заявке на химию'
        verbose_name_plural = 'Комментарии к заявке на химию'

# справочник оплат (платежей по QR коду)
class Payment (models.Model):
    date = models.DateTimeField('Дата/Время', null=True) #дата платежа
    summa = models.FloatField('Сумма', null=True) #сумма платежа
    zakaz_date = models.DateField('Дата заказа', null=True) #дата заказа
    zakaz_number = models.CharField('Номер заказа', max_length=30, default='', null=True) # № заказа
    zakaz_content = models.CharField('Содержание заказа', max_length=200, default='', null=True) # Содержание заказа
    status = models.BooleanField(default=True) #статус выполнен/невыполнен

    class Meta:
        verbose_name = 'Оплата по QR коду'
        verbose_name_plural = 'Платежи по QR кодам'

class Review (models.Model):
    date = models.DateField(null=True) #дата отзыва
    text = models.TextField(max_length=300, verbose_name='Содержание отзыва', default='', null=True)
    status = models.BooleanField(default=False) #статус принят/непринят
    user_exe = models.CharField(max_length=30, verbose_name='Пользователь', default='', null=True) #пользователь который принял отзыв
    time_exe = models.DateTimeField(null=True, verbose_name='Дата/время отработки', auto_now=True)
    maker = models.CharField(max_length=60, verbose_name='Создатель', default='', null=True)
    maker_tel = models.CharField(max_length=30, verbose_name='Телефон', default='', null=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'

class Podrazd (models.Model):
    name = models.CharField(max_length=50, verbose_name='Подразделение', default='', null=True) 

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

class Vidnach (models.Model):
    name = models.CharField(max_length=50, verbose_name='Вид начисления', default='', null=True) 

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Вид начисления'
        verbose_name_plural = 'Виды начисления'

class Vidmer (models.Model):
    name = models.CharField(max_length=50, verbose_name='Вид мероприятия', default='', null=True) 

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Вид мероприятия'
        verbose_name_plural = 'Виды мероприятий'

class Vidopl (models.Model):
    name = models.CharField(max_length=50, verbose_name='Вид оплаты', default='', null=True) 

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Вид оплаты'
        verbose_name_plural = 'Виды оплаты'

class Sotr (models.Model):
    name = models.CharField(max_length=50, verbose_name='Сотрудник', default='', null=True) 
    stavka = models.IntegerField('Ставка', default=0, null=True)
    ei = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Ед.') #ссылка на единицу измерения
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на место где он работает
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на подразделение где он работает
    active = models.BooleanField('Active', default=True, null=True, blank=True)
    img = models.ImageField('Изображение', upload_to='static/IMG', default='', null=True, max_length=200, blank=True)  #изображение

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Tabel (models.Model):
    date = models.DateField(null=True) #дата табеля
    sotr = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Сотрудник') #ссылка на сотрудника
    ei = models.ForeignKey('Ei', on_delete=models.CASCADE, null=True, verbose_name='Е.И.') #ссылка на единицу измерения
    kol = models.FloatField('Количество', default=0, null=True)
    sum = models.FloatField('Сумма', default=0, null=True)
    stavka = models.FloatField('Ставка', default=0, null=True)
    vidnach = models.ForeignKey('Vidnach', on_delete=models.CASCADE, null=True, verbose_name='Вид начисл.')
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на подразделение где он работает
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на место где он работает
    avtor = models.CharField(max_length=30, null=True, verbose_name='Автор')
    datecreated = models.DateTimeField(null=True) #дата создания табеля
    # t1 = models.DateTimeField(null=True, verbose_name='t Приход', blank=True)
    # t2 = models.DateTimeField(null=True, verbose_name='t Уход', blank=True)
    t1 = models.CharField(max_length=10, null=True, verbose_name='t Приход', blank=True)
    t2 = models.CharField(max_length=10, null=True, verbose_name='t Уход', blank=True)

    class Meta:
        verbose_name = 'Табель'
        verbose_name_plural = 'Табели'

class Vipl (models.Model):
    date = models.DateField(null=True) #дата выплаты
    sotr = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Сотрудник') #ссылка на сотрудника
    sum = models.FloatField('Сумма', default=0, null=True)
    vidnach = models.ForeignKey('Vidnach', on_delete=models.CASCADE, null=True, verbose_name='Вид начисл.')
    #avtor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор')
    avtor = models.CharField(max_length=30, null=True, verbose_name='Автор')
    datecreated = models.DateTimeField(null=True) #дата создания табеля

    class Meta:
        verbose_name = 'Выплата'
        verbose_name_plural = 'Выплаты'

class Den (models.Model):
    date = models.DateField(null=True) #дата рабочего дня
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на объект
    vnal = models.FloatField('Выручка Нал.', default=0, null=True)
    vbnal = models.FloatField('Выручка Б/Нал.', default=0, null=True)
    vbc = models.FloatField('Выручка БС.', default=0, null=True) # Бонусный счет
    vpp = models.FloatField('Выручка П/П', default=0, null=True) # Питание персонала
    vpr = models.FloatField('Выручка Предс.', default=0, null=True) # Представительские
    vsert = models.FloatField('Выручка Сертификат.', default=0, null=True) # Оплата сертификатом
    vb = models.FloatField('Выручка Бар', default=0, null=True) # Бар
    vk = models.FloatField('Выручка Кух.', default=0, null=True) # Кухня
    chn = models.FloatField('Чай/Нал.', default=0, null=True) # Чай нал
    chbn = models.FloatField('Чай/БНал.', default=0, null=True) # Чай Б/Н
    kolg = models.FloatField('Кол.гостей', default=0, null=True) # Кол гостей
    kolblud = models.FloatField('Кол.блюд', default=0, null=True) # Кол блюд
    masblud = models.FloatField('Масса блюд', default=0, null=True) # Масса блюд
    avtor = models.CharField(max_length=30, null=True, verbose_name='Автор')
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Создал', related_name="Создал") # Автор    
    datecreated = models.DateTimeField(null=True) #дата создания записи

    gorv = models.FloatField('Горячее', default=0, null=True) # Горячее
    gork = models.FloatField('Горячее, Кол', default=0, null=True) # Горячее, Кол-во
    holv = models.FloatField('Холодное', default=0, null=True) # Холодное
    holk = models.FloatField('Холодное, Кол', default=0, null=True) # Холодное, Кол-во
    pizv = models.FloatField('Пицца', default=0, null=True) # Пицца
    pizk = models.FloatField('Пицца, Кол', default=0, null=True) # Пицца, Кол-во
    alkv = models.FloatField('Алкоголь', default=0, null=True) # Алкоголь
    alkk = models.FloatField('Алкоголь, Кол', default=0, null=True) # Алкоголь, Кол-во
    desv = models.FloatField('Дессерт', default=0, null=True) # Дессерт
    desk = models.FloatField('Дессерт, Кол', default=0, null=True) # Дессерт, Кол-во
    kofv = models.FloatField('Кофе/Чай', default=0, null=True) # Кофе/Чай
    kofk = models.FloatField('Кофе/Чай, Кол', default=0, null=True) # Кофе/Чай, Кол-во

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'

class Banket (models.Model):
    date = models.DateField(null=True) #дата мероприятия банкета
    sum = models.IntegerField('Сумма', default=0, null=True)
    vidopl = models.ForeignKey('Vidopl', on_delete=models.CASCADE, null=True, verbose_name='Вид оплаты.', related_name="opl") #ссылка на вид оплаты
    predoplata = models.IntegerField('Предоплата', default=0, null=True)
    vidoplp = models.ForeignKey('Vidopl', on_delete=models.CASCADE, null=True, verbose_name='Вид оплаты предоплата', related_name="oplp") #ссылка на вид оплаты предоплата
    ssbor = models.IntegerField('С.Сбор', default=0, null=True)
    psbor = models.CharField(max_length=50, null=True, verbose_name='ПСбор')
    kolg = models.IntegerField('Кол.гостей', default=0, null=True) # Кол гостей
    vidmer = models.ForeignKey('Vidmer', on_delete=models.CASCADE, null=True, verbose_name='Вид меропр.') #ссылка на вид мероприятия
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на объект
    customer = models.CharField(max_length=50, null=True, verbose_name='Заказчик')
    contact = models.CharField(max_length=50, null=True, verbose_name='Контакт')
    remark = models.TextField(max_length=300, null=True, default='', verbose_name='Комментарий')
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name="author") # Автор
    datecreated = models.DateTimeField(null=True) #дата создания записи
    active = models.BooleanField('Active', default=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Банкет'
        verbose_name_plural = 'Банкеты'

class CauseList (models.Model):
    name = models.CharField('Причина', max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Причина'
        verbose_name_plural = 'Причины'

class MenuList (models.Model):
    name = models.CharField('Блюдо', max_length=150)
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

class StopList (models.Model):
    datecreated = models.DateTimeField(null=False) #дата/время внесения
    status = models.BooleanField(default=True) #статус находится/нет
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name="autor") #ссылка на сотрудника
    menu = models.ForeignKey('MenuList', on_delete=models.CASCADE, null=True, verbose_name='Блюдо') #ссылка на Блюдо
    cause = models.ForeignKey('CauseList', on_delete=models.CASCADE, null=True, verbose_name='Причина') #ссылка на Причину
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект
    causeinfo = models.CharField(max_length=150, null=True, verbose_name='Информация')
    autor_exe = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Исключил автор', related_name="autor_exe") #пользователь который убрал блюдо из Stop List
    date_exe = models.DateTimeField(null=True, verbose_name='Дата/время исключения', auto_now=True)
    ost = models.IntegerField ('Остаток', default=0, null=True) # Остаток, по умолчанию 0

    class Meta:
        verbose_name = 'Стоп лист'
        verbose_name_plural = 'Стоп лист'

class StopListRemark (models.Model):               # комментарий в стоп листе
    datecreated = models.DateTimeField(null=False) #дата/время внесения
    status = models.BooleanField(default=True) #статус находится/нет
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name="autor1") #ссылка на сотрудника
    remark = models.CharField(max_length=50, null=True, verbose_name='Комментарий')
    cause = models.ForeignKey('CauseList', on_delete=models.CASCADE, null=True, verbose_name='Причина') #ссылка на Причину
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект
    causeinfo = models.CharField(max_length=150, null=True, verbose_name='Информация')
    autor_exe = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Исключил автор', related_name="autor_exe1") #пользователь который убрал блюдо из Stop List
    date_exe = models.DateTimeField(null=True, verbose_name='Дата/время исключения', auto_now=True)
    ost = models.IntegerField ('Остаток', default=0, null=True) # Остаток, по умолчанию 0

    class Meta:
        verbose_name = 'Стоп лист комментарий'
        verbose_name_plural = 'Стоп лист комментарий'

# Справочник позиций сотрудников в графике
class Position (models.Model):
    name = models.CharField('Название должности', max_length=60, db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'       

class Graphic (models.Model):
    date = models.DateField(null=False, verbose_name='Дата') # Дата в графике
    status = models.BooleanField(default=True, verbose_name='Статус') #статус в графике/нет
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект Марта/EL Gusto
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на Подразделение Кухня/Бар
    sotr = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Сотрудник') #ссылка на Сотрудника
    pos = models.ForeignKey('Position', on_delete=models.CASCADE, null=True, verbose_name='Позиция') #ссылка на позицию сотрудника
    t1 = models.CharField(max_length=10, null=True, verbose_name='t Приход', blank=True)
    t2 = models.CharField(max_length=10, null=True, verbose_name='t Уход', blank=True)
    kol = models.FloatField('Количество', default=0, null=True) # Кол-во часов
    sum = models.FloatField('Сумма', default=0, null=True) # Кол-во денег от часов
    autor = models.CharField(max_length=30, null=True, verbose_name='Автор')
    datecreated = models.DateTimeField(null=True, verbose_name='Создание') #дата создания записи
    ch_autor = models.CharField(max_length=30, null=True, verbose_name='Автор изм.')
    datechanged = models.DateTimeField(null=True) #дата изменения записи

    class Meta:
        verbose_name = 'График сотрудников'
        verbose_name_plural = 'График сотрудников'

class UploadTaskImages(models.Model):
    taskpk = models.ForeignKey('ChListTask', on_delete=models.CASCADE, null=True, verbose_name='Задача', blank=True)
    unumber = models.IntegerField('UNumber', null=True, blank=True, default=None)
    img = models.ImageField('Image', upload_to='static/photo/%Y-%m-%d/', default=None, blank=True, null=True, max_length=100)

    def __str__(self) -> str:
        return self.img

    class Meta:
        verbose_name = 'Изображения задач'

class VisitControl (models.Model):

    dt_in = models.DateTimeField(null=False, verbose_name='Дата приход') # Дата/время прихода
    dt_out = models.DateTimeField(null=False, verbose_name='Дата уход') # Дата/время прихода
    status = models.BooleanField(default=True, verbose_name='Статус') #статус 0 пришел, 1 ушел
    sotr = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Сотрудник') #ссылка на Сотрудника
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект Марта/EL Gusto
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на Подразделение Кухня/Бар

    class Meta:
        verbose_name = 'Учет посещений сотрудников'
        verbose_name_plural = 'Учет посещений сотрудников'

class STaskStatus (models.Model):
    
    name = models.CharField('Статус', max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы задач'

class STaskPriority (models.Model):
    
    name = models.CharField('Приоритет', max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты задач'

class STaskType (models.Model):
    
    name = models.CharField('Тип', max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы задач'

# Справочник задач новый
class STask (models.Model):
    
    name = models.CharField('Описание задачи', max_length=200)
    date = models.DateTimeField(null=False, verbose_name='Дата/Время постановки') # Дата/время постановки
    creator = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Создатель') #ссылка на Создателя
    executor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Исполнитель', related_name="executor01") #ссылка на Исполнителя
    img = models.ImageField('Image', upload_to='static/photo/%Y-%m-%d/', default=None, blank=True, null=True, max_length=100)
    obj = models.ForeignKey('Receiver', on_delete=models.CASCADE, null=True, verbose_name='Объект') #ссылка на Объект Марта/EL Gusto
    div = models.ForeignKey('Podrazd', on_delete=models.CASCADE, null=True, verbose_name='Подразделение') #ссылка на Подразделение Кухня/Бар/Офис
    type = models.ForeignKey('STaskType', on_delete=models.CASCADE, null=True, verbose_name='Тип') #ссылка на Тип задач
    priority = models.ForeignKey('STaskPriority', on_delete=models.CASCADE, null=True, verbose_name='Приоритет') #ссылка на Приоритет задач
    dateexecution = models.DateField(null=True, verbose_name='Дата исполнения') # Дата исполнения
    daterenewal = models.DateField(null=True, verbose_name='Дата продления') # Дата продления
    status = models.ForeignKey('STaskStatus', on_delete=models.CASCADE, null=True, verbose_name='Статус') #ссылка на статус
    executorpassed = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Передано Исполнителю', related_name="executor02") #ссылка на передано Исполнителю
    active = models.BooleanField(default=True) #статус выполнен/невыполнен, активный/неактивный, по умолчанию активный (при создании)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи сотрудников'

class STaskExe (models.Model): #  Выполнение задачи, изменение статуса
    
    name = models.CharField('Выполнение', max_length=80)
    date = models.DateTimeField(null=True, verbose_name='Дата/Время выполнения') # Дата/время выполнения
    task = models.ForeignKey('STask', on_delete=models.CASCADE, null=True, verbose_name='Задача') #ссылка на задачу
    status = models.ForeignKey('STaskStatus', on_delete=models.CASCADE, null=True, verbose_name='Статус') #ссылка на статус
    img = models.ImageField('Image', upload_to='static/photo/%Y-%m-%d/', default=None, blank=True, null=True, max_length=100)
    executor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Исполнитель', related_name="executor") #ссылка на Исполнителя
    executorpassed = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Передано Исполнителю', related_name="executor1") #ссылка на передано Исполнителю
    priority = models.ForeignKey('STaskPriority', on_delete=models.CASCADE, null=True, verbose_name='Приоритет') #ссылка на приоритет новый

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Выполнение задачи'
        verbose_name_plural = 'Выполнение задач'

# Метрики KPI
class Kpimetric (models.Model):
    
    name = models.CharField('Описание метрики', max_length=200)
    kol = models.IntegerField ('Вес', default=0, null=True) # Вес метрики

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Метрика KPI'
        verbose_name_plural = 'Метрики KPI'

class Kpi (models.Model):
    
    date = models.DateTimeField(null=False, verbose_name='Дата/Время постановки') # Дата/время постановки
    name = models.CharField('Описание', default='', null=True, max_length=100)
    metric = models.ForeignKey('Kpimetric', on_delete=models.CASCADE, null=True, verbose_name='Метрика KPI') #ссылка на метрику KPI
    autor = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Автор', related_name="Sotr00") #ссылка на Автора
    sotr = models.ForeignKey('Sotr', on_delete=models.CASCADE, null=True, verbose_name='Сотрудник', related_name="Sotr01") #ссылка на Сотрудника для которого определяется метрика
    kol = models.IntegerField ('Вес', default=0, null=True) # Вес метрики
    active = models.BooleanField(default=True) #статус активна/неактивна, по умолчанию активный (при создании)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Показатель KPI'
        verbose_name_plural = 'Показатели KPI'
