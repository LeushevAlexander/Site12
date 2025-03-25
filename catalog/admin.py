from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.forms import TextInput
from django.db import models 

# Register your models here.
from .models import Task #список задач на выполнение
from .models import JobTitle #должности
from .models import CheckListTaskItem  #записи в чек листах

from .models import ChList #  справочник чек листов
from .models import ChListRec #  справочник записей по чек листу
from .models import ChListTask #  справочник заданий по записям в чек листе

from .models import Ei # Единицы измерения
from .models import Source # Места закупа
from .models import Receiver # Объекты производства
from .models import Nomen # Номенклатура
from .models import NomenHim # Номенклатура химия
from .models import Zakaz # Заявки на продукты/материалы
from .models import ZakazHim # Заявки на химию
from .models import Zakazremark # Коментарии к заявкам на продукты/материалы
from .models import ZakazremarkHim # Коментарии к заявкам на химию
from .models import Payment # Регистрация платежей по QR коду
from .models import Review # Обратный отзыв
from .models import Sotr # Сотрудники
from .models import Vidnach # Вид начислений
from .models import Podrazd # Подразделения
from .models import Vidmer # Вид мероприятия
from .models import Vidopl # Вид оплаты
from .models import Tabel # Табель
from .models import Vipl # Выплаты
from .models import Den # Рабочий день
from .models import Banket # Банкет
from .models import CauseList # Список причин постановки в стоп лист
from .models import MenuList # Список блюд в меню 
from .models import StopList # Стоп лист
from .models import Graphic # График выхода сотрудников
from .models import Position # Позиции сотрудников

from .models import STask # Задачи
from .models import STaskPriority # Задачи приоритет
from .models import STaskType # Задачи приоритет
from .models import STaskExe # Задачи Выполнение
from .models import STaskStatus # Статус заданий

from django.utils.safestring import mark_safe

class ItemInline(admin.TabularInline):
    model = CheckListTaskItem
    extra = 1
    verbose_name = 'Задача по чек-листу'
    verbose_name_plural = 'Список задач по чек-листу'

class TaskJobTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'jobtitle')
    list_display_links = ('id', 'name', 'jobtitle')
    inlines = [ItemInline]
    save_on_top = True
    # 'Список задач по чек-листу'

class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'jobtitlename')   
    list_display_links = ('id', 'jobtitlename')   

class TaskExeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'tasklink', 'jobtitlelink', 'taskjobtitlelink', 'time_control', 'order', 'status', 'user_exe', 'time_exe') 
     
# Новое !!!!
class ItemInChl(admin.TabularInline):  # Запись по чек листу

    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'100'})}
}    
    model = ChListRec
    show_change_link = False
    extra = 0
    verbose_name = 'Задача по чек-листу'
    verbose_name_plural = 'Список задач по чек-листу'
    fields = ['order', 'name', ('t1', 't2')]

class ChListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'obj', 'div', 't1', 't2', 'u1', 'u2', 'u3')
    list_display_links = ('id', 'name', 'obj', 'div', 't1', 't2', 'u1', 'u2', 'u3')

    fields = ['name', ('obj', 'div'), ('t1', 't2'), ('u1', 'u2', 'u3')]

    inlines = [ItemInChl]
    save_on_top = True

class ChListTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'chl', 'chlrec', 'obj', 'div', 'autor', 'created') 
    list_display_links = ('id', 'date', 'chl', 'chlrec', 'obj', 'div', 'autor', 'created') 


class EiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class NomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'source_link', 'name', 'ei', 'cost', 'img')
    list_display_links = ('id', 'order', 'name', 'cost')
    search_fields = ('name', 'id')
    readonly_fields = ("get_img", )

    def get_img(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="350" height="300"') #width="80" height="100"
    
    get_img.short_description = "Изображение"

class NomenHimAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'source_link', 'name', 'ei', 'cost', 'img')
    list_display_links = ('id', 'order', 'name', 'cost')
    search_fields = ('name', 'id')
    readonly_fields = ("get_img", )

    def get_img(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="350" height="300"') #width="80" height="100"
    
    get_img.short_description = "Изображение"

class ZakazAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'source_link', 'receiver_link', 'nomen_link', 'ei_link', 'kol', 'cost', 'creator', 'time_create', 'maker', 'time_make', 'deliver', 'time_deliv')
    list_display_links = ('id', 'status', 'date', 'kol', 'cost', 'creator', 'time_create', 'maker', 'time_make', 'deliver', 'time_deliv')

class ZakazHimAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'source_link', 'receiver_link', 'nomen_link', 'ei_link', 'kol', 'cost', 'creator', 'time_create', 'maker', 'time_make', 'deliver', 'time_deliv')
    list_display_links = ('id', 'status', 'date', 'kol', 'cost', 'creator', 'time_create', 'maker', 'time_make', 'deliver', 'time_deliv')

class ZakazremarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'remark', 'creator', 'time_create', 'maker', 'time_make')
    list_display_links = ('id', 'status', 'date', 'remark', 'creator', 'time_create', 'maker', 'time_make')

class ZakazremarkHimAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'remark', 'creator', 'time_create', 'maker', 'time_make')
    list_display_links = ('id', 'status', 'date', 'remark', 'creator', 'time_create', 'maker', 'time_make')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'summa', 'zakaz_date', 'zakaz_number', 'zakaz_content')
    list_display_links = ('id', 'status', 'date', 'summa', 'zakaz_date', 'zakaz_number', 'zakaz_content')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date', 'text', 'user_exe', 'time_exe')
    list_display_links = ('id', 'status', 'date', 'text', 'user_exe', 'time_exe')

class SotrAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'obj', 'stavka', 'ei', 'active')
    list_display_links = ('id', 'name', 'obj', 'stavka', 'ei', 'active')
    ordering = ('name',)

class PodrazdAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class VidnachAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class VidmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class VidoplAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class TabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'sotr', 'ei', 'stavka', 'kol', 'sum', 'vidnach', 'avtor', 'datecreated')
    list_display_links = ('id', 'date', 'sotr', 'ei', 'stavka', 'kol', 'sum', 'vidnach', 'avtor', 'datecreated')
    search_fields = (['date'])

class ViplAdmin(admin.ModelAdmin):
    list_display = ('id', 'sotr', 'vidnach', 'sum', 'avtor', 'datecreated')
    list_display_links = ('id', 'sotr', 'vidnach', 'sum', 'avtor', 'datecreated')

class DenAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'obj', 'vnal', 'vbnal', 'vb', 'vk', 'kolg', 'kolblud', 'masblud', 'avtor', 'datecreated')
    list_display_links = ('id', 'date', 'obj', 'vnal', 'vbnal', 'vb', 'vk', 'kolg', 'kolblud', 'masblud', 'avtor', 'datecreated')

class BanketAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'sum', 'ssbor', 'kolg', 'vidmer', 'customer', 'contact', 'autor', 'datecreated')
    list_display_links = ('id', 'date', 'sum', 'ssbor', 'kolg', 'vidmer', 'customer', 'contact', 'autor', 'datecreated')

class CauseListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class MenuListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'obj')
    list_display_links = ('id', 'name', 'obj')

class StopListAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'datecreated', 'menu', 'ost', 'cause', 'obj', 'autor', 'date_exe', 'autor_exe', 'causeinfo')
    list_display_links = ('id', 'status', 'datecreated', 'menu', 'ost', 'cause', 'obj', 'autor', 'date_exe', 'autor_exe', 'causeinfo')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class GraphicAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'sotr', 'pos', 'obj', 'div', 'pos', 't1', 't2', 'kol', 'sum', 'datecreated', 'autor', 'datechanged', 'ch_autor')
    list_display_links = ('id', 'date', 'status', 'sotr', 'pos', 'obj', 'div', 'pos', 't1', 't2', 'kol', 'sum', 'datecreated', 'autor', 'datechanged', 'ch_autor')

class STaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class STaskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class STaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class STaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'name', 'status',  'creator', 'type', 'obj', 'div', 'priority')
    list_display_links = ('id', 'name', 'status',  'creator', 'type', 'obj', 'div', 'priority')

admin.site.register(Task)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(ChList, ChListAdmin)
admin.site.register(ChListTask, ChListTaskAdmin)
admin.site.register(Ei, EiAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(Nomen, NomenAdmin)
admin.site.register(Zakaz, ZakazAdmin)
admin.site.register(Zakazremark, ZakazremarkAdmin)
admin.site.register(NomenHim, NomenHimAdmin)
admin.site.register(ZakazHim, ZakazHimAdmin)
admin.site.register(ZakazremarkHim, ZakazremarkHimAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Sotr, SotrAdmin)
admin.site.register(Podrazd, PodrazdAdmin)
admin.site.register(Vidnach, VidnachAdmin)
admin.site.register(Vidmer, VidmerAdmin)
admin.site.register(Tabel, TabelAdmin)
admin.site.register(Vipl, ViplAdmin)
admin.site.register(Den, DenAdmin)
admin.site.register(Banket, BanketAdmin)
admin.site.register(Vidopl, VidoplAdmin)
admin.site.register(CauseList, CauseListAdmin)
admin.site.register(MenuList, MenuListAdmin)
admin.site.register(StopList, StopListAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Graphic, GraphicAdmin)
admin.site.register(STaskStatus, STaskStatusAdmin)
admin.site.register(STaskType, STaskTypeAdmin)
admin.site.register(STaskPriority, STaskPriorityAdmin)
admin.site.register(STask, STaskAdmin)

admin.site.site_header = "Администрирование"

