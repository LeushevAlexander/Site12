from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.core.serializers import serialize
from django.db.models import Count, Sum, Q
from django.utils import timezone

from .views import getmenu
from .forms import AddChListRecForm, ChlWorkForm, ChlControlForm, ChlReportBasicForm, ChlControlTaskProblemForm, UploadFileForm, ChlReportControlForm, KPITaskReportForm
from .models import ChList, ChListRec, ChListTask, Receiver, Tabel, Podrazd, Sotr, UploadTaskImages

import datetime
#from datetime import datetime, date, timedelta

def SotrTabelInfo ( dt, obj, div): # Функция, которая возвращает структуру с данными о работающих сотрудниках
    
    mas = []

    #  делаем запрос в таблице табеля
    t = Tabel.objects.filter(date=dt, obj=obj, div=div)
    for v in t:
        
        if (v.sotr is not None):

            if (v.t1 is not None):
                s = str (v.sotr.name) + ' (' + v.t1 + '-' + v.t2 + ')'
                rec = {
                    'sotrdata': s,
                }
                mas.append(rec)
    
    return mas

def ChListRecInfo ( dt, chlist ): # Функция, которая возвращает структуру с данными о выполнении/контроле по чек листам
    
    s = ''
    # дата уже в формате datetime, т.е. можно сразу делать запрос
    r = ChListTask.objects.filter(date=dt, chl=chlist )

    vip = 0
    con = 0
    cis = 0
    fail = 0

    for v in r:
        # считаем, сколько выполнили, сколько проконтролировали, сколько провалены в контроле, причем по участкам, которые в чек листе
        if v.chl.u1 is not None:        
            if len (str(v.chl.u1)) > 0:
                cis = cis + 1
                if v.f1:
                    vip = vip + 1
                
                if v.cf1:
                    con = con + 1

                if not v.cst1:
                    fail += 1
                    
        if v.chl.u2 is not None:        
            if len (str(v.chl.u2)) > 0:
                cis = cis + 1
                if v.f2:
                    vip = vip + 1
                
                if v.cf2:
                    con = con + 1

                if not v.cst2:
                    fail += 1


        if v.chl.u3 is not None:        
            if len (str(v.chl.u3)) > 0:
                cis = cis + 1
                if v.f3:
                    vip = vip + 1
                
                if v.cf3:
                    con = con + 1

                if not v.cst3:
                    fail += 1

    if fail == 0:
        fail = ''
    else:
        fail = '(' + str(fail) + ')'

    s = { 
        'vip': vip,
        'con': con,
        'cis': cis,
        'fail': fail,
    }

    return s


def ChListRecCreated ( dt, chlist ):  # Функция, которая возвращает структуру, созданы ли записи по чек-листам на эту дату, 

    # дата уже в формате datetime, т.е. можно сразу делать запрос

    s = ''
    r = ChListTask.objects.filter(date=dt, chl=chlist )
    for v in r:
        # считываем наличие, кто создал, время
        autorname = ''
        if v.autor is not None:
            autorname = v.autor.name

        #t = v.created
        #t = f'{v.created.astimezone():%Y-%m-%d, %H:%M}'
        t = f'{v.created:%H:%M}'

        #  В наименование добавляю участки для отметки
        a = '('
        if v.chl.u1 is not None:        
            if len (str(v.chl.u1)) > 0:
                a += v.chl.u1
        
        if v.chl.u2 is not None:         
            if len (str(v.chl.u2)) > 0:
                a += ' ,'
                a += v.chl.u2
        if v.chl.u2 is not None:                
            if len (str(v.chl.u3)) > 0:
                a += ' ,'
                a += v.chl.u3        

        a += ')'

        s = {'ChList': (v.chl.name + a), 'Autor': autorname, 'Time': t}
        break

    return s
    

def AddChListRec(Request):

    cmas = []
    omas = []

    mn = getmenu(Request)

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    usr = Request.user
    sotr = usr.sotr # Сотрудник
    ob = sotr.obj # объект, к которому относится сотрудник, по умолчанию сначала он

    # список объектов
    omas = Receiver.objects.all ()

    # Делаем список чек листов, по которым уже созданы записи c фильтром по объектам
    # таблицу по чек листам, заполнены / нет
    chl = ChList.objects.filter(obj=ob)

    n = 1
    for w in chl:

        maked = 0
        aut = ''
        dtm = ''

        r = ChListRecCreated ( tdate, w )
        s = ChListRecInfo ( tdate, w )

        a = ''
        if len (r) > 0: 
            maked = 1
            aut = r['Autor']
            dtm = r['Time']
            a = '(' + aut + ', ' + dtm + ')'

        rec = {
            'number': n,
            'chl': w,
            'maked': maked,
            'autor': a,
            'vip': str (s['vip']),
            'con': str (s['con']),
            'cis': str (s['cis']),
            'fail': str (s['fail']),
        }

        cmas.append (rec)
        n = n + 1

    if Request.method == 'POST':
    
        form = AddChListRecForm(Request.POST)
        
        if form.is_valid():


            # Нажали кнопку "Обновить"
            
            # Нужно создать записи по чек листам на выполнение
            # Определяем выбранный чек лист
            # определяем сотрудника
            # Определяем время

            ob = Request.POST['ob_field']
            ob = Receiver.objects.get(pk=ob)
            dt = Request.POST['chl_date']
            tdate = dt
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                        
            cmas =[]
            # Делаем список чек листов, по которым уже созданы записи c фильтром по объектам
            # таблицу по чек листам, заполнены / нет
            chl = ChList.objects.filter(obj=ob)
            n = 1

            for w in chl:

                maked = 0
                aut = ''
                dtm = ''

                r = ChListRecCreated ( dt, w )
                s = ChListRecInfo ( tdate, w )
                a = ''

                if len (r) > 0: 
                    maked = 1
                    aut = r['Autor']
                    dtm = r['Time']
                    a = '(' + aut + ', ' + dtm + ')'

                rec = {
                        'number': n,
                        'chl': w,
                        'maked': maked,
                        'autor': a,
                        'vip': str (s['vip']),
                        'con': str (s['con']),
                        'cis': str (s['cis']),
                        'fail': str (s['fail']),
                    }

                cmas.append (rec)
                n = n + 1

    
    form = AddChListRecForm ()    

    return render(Request, 'catalog/addchlistrec.html', {'form': form, 'menu': mn, 
            'title': 'Чек листы', 'cmas': cmas, 'omas': omas, 'date_chl': tdate, 'obj': ob, })

def CreateChlTaskRec (Request, chlpk):

    # l = len(chlpk)

    # определяем чек лист  pk
    cpk = int(chlpk) # id записи
    usr = Request.user.sotr
    dt = datetime.datetime.now()
    
    # делаем обход по чек листу и создаем записи с заданиями
    w = ChList.objects.filter(pk=cpk)
    
    for v in w:

        # Проверяю, созданы ли записи
        k = ChListRecCreated ( dt, v )
        if len (k) == 0:
            chlrec = ChListRec.objects.filter(chl=v).order_by('order')
            for r in chlrec:
                # Создаем запись
                task = ChListTask (date=dt, chl=v, chlrec=r, obj=v.obj, div=v.div, autor=usr, created=dt)
                task.save()


    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})


def SetChlTask (Request, taskpk):
    l = len(taskpk)
    s = taskpk[:l-1]
    s1 = taskpk[l-1:l]

    # ставим галочку о выполнении
    f = int(s1)  # номер поля
    pk = int(s) # id записи
    usr = Request.user.sotr
    dt = datetime.datetime.now()

    # обновляем запись
    if (f == 1):
        r = ChListTask.objects.filter(pk=pk).update(f1=True, s1=usr, t1=dt)
    elif (f == 2):
        r = ChListTask.objects.filter(pk=pk).update(f2=True, s2=usr, t2=dt)
    elif (f == 3):
        r = ChListTask.objects.filter(pk=pk).update(f3=True, s3=usr, t3=dt)

    
#    t=int(task_id)
#    us=Request.user.username
#    r = TaskExe.objects.filter(id=t).update(status=True, user_exe=us, time_exe=datetime.datetime.now())
    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})


def ChlWork (Request):
    
    # работа по чек листу
    # в загловке выбираем дату, чек лист и делаем отметки по участкам
    # Соответственно заполняются данные кто отметил, когда и на каком участке

    chltask = []
    spr = []
    uch = [] # список участков
    mn = getmenu(Request)

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'  # по умолчанию, сегодняшняя
    
    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    usr = Request.user
    sotr = Request.user.sotr # Сотрудник

    clist = ChList.objects.all() # Список чек листов

    # Делаем список чек листов, по которым уже созданы записи
    for c in clist:
        r = ChListRecCreated ( tdate, c )
        if len(r) > 0:
            spr.append(r)

    if Request.method == 'POST':
        form = AddChListRecForm(Request.POST)
        
        if form.is_valid():

            # Нужно создать записи по чек листам на выполнение
            # Определяем выбранный чек лист
            # определяем сотрудника
            # Определяем время
            
            chl = Request.POST['chl']
            chl = ChList.objects.get(id=chl)
            d = Request.POST['chl_date']
            tdate = d
            d = datetime.datetime.strptime(d, '%Y-%m-%d')
            n = 1            

            # делаем обход по записям с заданиями и заполняем таблицу
            w = ChListTask.objects.filter(chl=chl.pk, date=d).order_by('pk')

            # устанавливаю количество полей и наименования в заголовке
            k = 1  # количество участков

            for v in w:
                if (len(str(v.chl.u1)) > 0) & (v.chl.u1 is not None):
                    st = { 'name': v.chl.u1, 'number': 1 }
                    uch.append(st)

                if (len(str(v.chl.u2)) > 0) & (v.chl.u2 is not None):
                    st = { 'name': v.chl.u2, 'number': 2 }
                    uch.append(st)
                    k += 1

                if (len(str(v.chl.u3)) > 0) & (v.chl.u3 is not None):
                    st = { 'name': v.chl.u3, 'number': 3 }
                    uch.append(st)
                    k += 1

                break

            for v in w:
                # Заполняю массив с  заданиями
                st = { 'n': n, 'taskpk': v.pk, 'name': v.chlrec.name, 'f1': v.f1, 'f2': v.f2, 'f3': v.f3 }
                chltask.append(st); n += 1
    else:
        # чек лист по умолчанию выбираем первым
        for w in clist:
            chl = w
            break

    # Выводим список заданий по чек листу
    form = ChlWorkForm ()

    return render(Request, 'catalog/chlwork.html', {'form': form, 'menu': mn, 
            'title': 'Работа по Ч/Л', 'clist': clist, 'date_chl': tdate, 'slist': spr, 'task': chltask, 'uch': uch, 'setchl': chl.id })

def ChlGoWork (Request, chlpk, dt):

    chltask = []
    spr = []
    uch = [] # список участков
    mn = getmenu(Request)

    #  Переход на страницу выполнения чек листа

    pk = int(chlpk) # id записи чек листа
    tdate = datetime.datetime.strptime(dt, '%Y-%m-%d')

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    #   заполняем данные и выводим окно выполнения
    clist = ChList.objects.filter(pk=pk) # Список чек листов
   
    # Делаем список чек листов, по которым уже созданы записи
    for c in clist:
        r = ChListRecCreated ( tdate, c )
        if len(r) > 0:
            spr.append(r)

            chl = ChList.objects.get(id=pk)
            n = 1            

            # делаем обход по записям с заданиями и заполняем таблицу
            w = ChListTask.objects.filter(chl=chl.pk, date=tdate).order_by('pk')

            # устанавливаю количество полей и наименования в заголовке
            k = 1  # количество участков

            for v in w:
                if (len(str(v.chl.u1)) > 0) & (v.chl.u1 is not None):
                    st = { 'name': v.chl.u1, 'number': 1 }
                    uch.append(st)

                if (len(str(v.chl.u2)) > 0) & (v.chl.u2 is not None):
                    st = { 'name': v.chl.u2, 'number': 2 }
                    uch.append(st)
                    k += 1

                if (len(str(v.chl.u3)) > 0) & (v.chl.u3 is not None):
                    st = { 'name': v.chl.u3, 'number': 3 }
                    uch.append(st)
                    k += 1

                break

            for v in w:
                # Заполняю массив с  заданиями
                st = { 'n': n, 'taskpk': v.pk, 'name': v.chlrec.name, 'f1': v.f1, 'f2': v.f2, 'f3': v.f3 }
                chltask.append(st); n += 1

    # Выводим список заданий по чек листу
    form = ChlWorkForm ()

    return render(Request, 'catalog/chlwork.html', {'form': form, 'menu': mn, 
            'title': 'Работа по Ч/Л', 'clist': clist, 'date_chl': dt, 'slist': spr, 'task': chltask, 'uch': uch, 'setchl': pk })


def ChlControl (Request):
    
    # работа по проверке чек листов
    # в загловке выбираем дату, чек лист и делаем отметки по проверке участков
    # Соответственно заполняются данные кто проверил отметил, когда и на каком участке

    chltask = []
    spr = []
    uch = [] # список участков
    mn = getmenu(Request)

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'  # по умолчанию, сегодняшняя
    
    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    usr = Request.user
    sotr = Request.user.sotr # Сотрудник

    clist = ChList.objects.all() # Список чек листов

    # Делаем список чек листов, по которым уже созданы записи
    for c in clist:
        r = ChListRecCreated ( tdate, c )
        if len(r) > 0:
            spr.append(r)

    if Request.method == 'POST':
        form = ChlControlForm (Request.POST)
        
        if form.is_valid():

            # Нужно создать записи по чек листам на выполнение
            # Определяем выбранный чек лист
            # определяем сотрудника
            # Определяем время
            
            chl = Request.POST['chl']
            chl = ChList.objects.get(id=chl)
            d = Request.POST['chl_date']

            tdate = d

            d = datetime.datetime.strptime(d, '%Y-%m-%d')
            n = 1

            # делаем обход по записям с заданиями и заполняем таблицу
            w = ChListTask.objects.filter(chl=chl.pk, date=d).order_by('pk')

            # устанавливаю количество полей и наименования в заголовке
            k = 1  # количество участков

            for v in w:

                if (len(str(v.chl.u1)) > 0) & (v.chl.u1 is not None):

                    st = { 'name': v.chl.u1, 'number': 1 }
                    uch.append(st)

                if (len(str(v.chl.u2)) > 0) & (v.chl.u2 is not None):

                    st = { 'name': v.chl.u2, 'number': 2 }
                    uch.append(st)
                    k += 1

                if (len(str(v.chl.u3)) > 0) & (v.chl.u3 is not None):

                    st = { 'name': v.chl.u3, 'number': 3 }
                    uch.append(st)
                    k += 1

                break

            for v in w:
                
                # ищу фото в коллекции
                img1 = ''; img2 = ''; img3 = ''
                im = UploadTaskImages.objects.filter(taskpk__pk=v.pk) 

                for j in im:
                    if j.unumber == 1:
                        img1 = j.img
                    elif j.unumber == 2:
                        img2 = j.img
                    elif j.unumber == 3:
                        img3 = j.img
                
                # Заполняю массив с  заданиями и контролями
                st = { 'n': n, 'pk': v.pk, 'name': v.chlrec.name, 'f1': v.cf1, 'f2': v.cf2, 'f3': v.cf3, 
                        'obj': v.obj.name, 'sf1': v.cst1, 'sf2': v.cst2, 'sf3': v.cst3, 
                    'img1': img1, 'img2': img2, 'img3': img3, 'rem1': v.rem1, 'rem2': v.rem2, 'rem3': v.rem3 }
                
                chltask.append(st); n += 1
    else:
        # чек лист по умолчанию выбираем первым
        for w in clist:
            chl = w
            break

    # Выводим список заданий по чек листу
    form = ChlControlForm ()

    return render(Request, 'catalog/chlcontrol.html', {'form': form, 'menu': mn, 
            'title': 'Контроль по Ч/Л', 'clist': clist, 'date_chl': tdate, 'slist': spr, 'task': chltask, 'uch': uch, 'setchl': chl.id })

def ChlGoControl (Request, chlpk, dt):

    # открываем форму по контролю по конкретному чек листу за день
    
    chltask = []
    spr = []
    uch = [] # список участков
    mn = getmenu(Request)

    pk = int(chlpk) # id записи чек листа
    tdate = datetime.datetime.strptime(dt, '%Y-%m-%d')
   
    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    usr = Request.user
    sotr = Request.user.sotr # Сотрудник

    clist = ChList.objects.filter(pk=pk) # Список чек листов

    # Делаем список чек листов, по которым уже созданы записи
    for c in clist:
        r = ChListRecCreated ( tdate, c )
        if len(r) > 0:
            spr.append(r)

    form = ChlControlForm (Request.POST)
        

    # Нужно создать записи по чек листам на выполнение
    # Определяем выбранный чек лист
    # определяем сотрудника
    # Определяем время
            
    chl = ChList.objects.get(id=chlpk)
    n = 1

            # делаем обход по записям с заданиями и заполняем таблицу
    w = ChListTask.objects.filter(chl=chl.pk, date=tdate).order_by('pk')

    # устанавливаю количество полей и наименования в заголовке
    k = 1  # количество участков

    for v in w:
        if (len(str(v.chl.u1)) > 0) & (v.chl.u1 is not None):
            st = { 'name': v.chl.u1, 'number': 1 }
            uch.append(st)

        if (len(str(v.chl.u2)) > 0) & (v.chl.u2 is not None):
            st = { 'name': v.chl.u2, 'number': 2 }
            uch.append(st)
            k += 1

        if (len(str(v.chl.u3)) > 0) & (v.chl.u3 is not None):
            st = { 'name': v.chl.u3, 'number': 3 }
            uch.append(st)
            k += 1

        break

    for v in w:

        # ищу фото в коллекции
        img1 = ''; img2 = ''; img3 = ''
        im = UploadTaskImages.objects.filter(taskpk__pk=v.pk) 

        for j in im:
            if j.unumber == 1:
                img1 = j.img
            elif j.unumber == 2:
                img2 = j.img
            elif j.unumber == 3:
                img3 = j.img

        # Заполняю данные по отметке
        if v.s1 is not None:
            otm1 = str (str (v.s1.name) + ',' + f'{v.t1.astimezone():%Y-%m-%d, %H:%M}')
        else:
            otm1 = 'Нет отметки.'

        if v.s2 is not None:
            otm2 = str (str (v.s2.name) + ',' + f'{v.t2.astimezone():%Y-%m-%d, %H:%M}')
        else:
            otm2 = 'Нет отметки.'

        if v.s3 is not None:
            otm3 = str (str (v.s3.name) + ',' + f'{v.t3.astimezone():%Y-%m-%d, %H:%M}')
        else:
            otm3 = 'Нет отметки.'

        # Заполняю данные по контролю
        if v. cs1 is not None:
            con1 = str (str (v.cs1.name) + ',' + f'{v.ct1.astimezone():%Y-%m-%d, %H:%M}')
        else:
            con1 = 'Нет контроля.'

        if v. cs2 is not None:
            con2 = str (str (v.cs2.name) + ',' + f'{v.ct2.astimezone():%Y-%m-%d, %H:%M}')
        else:
            con2 = 'Нет контроля.'

        if v. cs3 is not None:
            con3 = str (str (v.cs2.name) + ',' + f'{v.ct2.astimezone():%Y-%m-%d, %H:%M}')
        else:
            con3 = 'Нет контроля.'

        # Заполняю массив с  заданиями и контролями
        st = { 'n': n, 'pk': v.pk, 'name': v.chlrec.name, 'f1': v.cf1, 'f2': v.cf2, 'f3': v.cf3, 
            'obj': v.obj.name, 'sf1': v.cst1, 'sf2': v.cst2, 'sf3': v.cst3, 
            'img1': img1, 'img2': img2, 'img3': img3, 'rem1': v.rem1, 'rem2': v.rem2, 'rem3': v.rem3,
             'otm1': otm1, 'otm2': otm2, 'otm3': otm3, 'con1': con1, 'con2': con2, 'con3': con3, }
        
        chltask.append(st); n += 1

    # Выводим список заданий по чек листу

    return render(Request, 'catalog/chlcontrol.html', {'form': form, 'menu': mn, 
            'title': 'Контроль по Ч/Л', 'clist': clist, 'date_chl': dt, 'slist': spr, 'task': chltask, 'uch': uch, 'setchl': pk })


def SetChlControlTask (Request, taskpk):
    l = len(taskpk)
    s = taskpk[:l-1]
    s1 = taskpk[l-1:l]

    # ставим галочку о выполнении
    f = int(s1)  # номер поля
    pk = int(s) # id записи
    usr = Request.user.sotr
    
    #dt = datetime.datetime.now()
    dt = timezone.now()

    # обновляем запись
    if (f == 1):
        r = ChListTask.objects.filter(pk=pk).update(cf1=True, cs1=usr, ct1=dt)
    elif (f == 2):
        r = ChListTask.objects.filter(pk=pk).update(cf2=True, cs2=usr, ct2=dt)
    elif (f == 3):
        r = ChListTask.objects.filter(pk=pk).update(cf3=True, cs3=usr, ct3=dt)
    
    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})

def SaveChlControlTaskRem (Request, taskpk, taskrem):
    
    l = len(taskpk)
    s = taskpk[:l-1]
    s1 = taskpk[l-1:l]

    # ставим галочку о выполнении
    f = int(s1)  # номер поля
    pk = int(s) # id записи
    usr = Request.user.sotr
    
    #dt = datetime.datetime.now()
    dt = timezone.now ()

   # обновляем запись при обновлении, ставим статус что есть проблема, сохраняем комментарий о проблеме

    if (f == 1):
        r = ChListTask.objects.filter(pk=pk).update(cf1=True, cs1=usr, ct1=dt, cst1=False, rem1=taskrem)
    elif (f == 2):
        r = ChListTask.objects.filter(pk=pk).update(cf2=True, cs2=usr, ct2=dt, cst2=False, rem2=taskrem)
    elif (f == 3):
        r = ChListTask.objects.filter(pk=pk).update(cf3=True, cs3=usr, ct3=dt, cst3=False, rem3=taskrem)
    
    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})

def handle_uploaded_file (f):
    with open (f'Img/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def ChlUploadImage (Request, taskpk):
    
    k = taskpk
    # загружаем изображение
    if Request.method == 'POST':

        if 'file_upload' in Request.FILES:        
            #handle_uploaded_file (Request.FILES['file_upload'])    
            # определяю задачу, определяю участок
            l = len(taskpk)
            s = taskpk[:l-1]
            s1 = taskpk[l-1:l]

            f = int(s1)  # номер поля
            p = int(s) # id записи

            ts = ChListTask.objects.get(pk = p)

            fl = UploadTaskImages(img=Request.FILES['file_upload'], unumber = f, taskpk = ts)
            fl.save()

            return HttpResponseRedirect('.')
        else:
            return HttpResponse (status=200)
    else:
        return HttpResponse (status=200)   

    
    #return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})
    #render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})
    #    return HttpResponseRedirect('.')
    #return HttpResponseRedirect(Request.META.get('HTTP_REFERER'))
    #return render (Request)
    #return HttpResponse (status=200)

def ChlTaskInfo (Request, taskpk):
    
    uchnumber = 1 # Номер участка

    # Сдесь мы заполняем изображение, описание проблемы по объекту
    l = len(taskpk)
    s = taskpk[:l-1]
    s1 = taskpk[l-1:l]
    uch = ''
    mn = getmenu(Request)

    # ставим галочку о выполнении
    f = int(s1)  # номер поля
    pk = int(s) # id записи
    usr = Request.user.sotr

    form = ChlControlTaskProblemForm ()

    # Отображаем полученню информацию
    taskobj = ChListTask.objects.get(pk=pk)
    chl = taskobj.chl
    

    # определяю участок
    if f == 1:
        if chl.u1 is not None:
            uch = chl.u1
        else:
            uch = ''
    elif f == 2:
        if chl.u2 is not None:
            uch = chl.u2
        else:
            uch = ''
    elif f == 3:
        if chl.u3 is not None:
            uch = chl.u3
        else:
            uch = ''

    uchnumber = 1

    if Request.method == 'POST':
        handle_uploaded_file (Request.FILES['file_upload'])


    # Вывожу окно с даными
    return render(Request, 'catalog/chltaskinfo.html', {'form': form, 'menu': mn, 'taskpk': taskpk, 
            'title': 'Описание проблемы', 'uch': uch, 'uchnumber': uchnumber, })

    




def ChlReportBasic (Request):

    #Отчет по чек листам основной
    usr = ''
    curobj = ''

    mn = getmenu(Request)
    dmas = [] # это массив подразделений
    smas = [] # это массив сотрудников, по часам
    cmas = [] # это массив неоткрытых чек листов
    omas = [] # это массив открытых чек листов
    rmas = [] # это массив несделанных записей в чек листах
    ormas = [] # это массив открытых чек листов, в которых есть несделанные записи
    ocmas = [] # это массив открытых чек листов, которых есть записи с ошибками, которые поставили контролеры
    cnmas = [] # это массив записей проверенных, с ошибками
    stmas = [] # это массив сотрудников, по которым выводятся данные по выполнению
    srmas = [] # это массив сотрудников с выполненными задачами

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    # Всем пользователям доступен этот отчет
    # if Request.user.A_Tabel != True:
    #     # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
    #     return redirect('AccessDenied') 

    ddate = datetime.date.today()

    ddate = f'{ddate:%Y-%m-%d}'
    obj = Receiver.objects.all()
    divis = Podrazd.objects.all()
    stmas = Sotr.objects.filter(active=True)

    # сначала делаем запрос с информацией о времени работы
    # в конце мы делаем такой же запрос но без времени, что ты в списке не было много одинаковой информации
    # и присоединяем ей информацию о времени ))

    rep = Tabel.objects.filter(date=ddate).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

    if Request.method == 'POST':
        
        formreport = ChlReportBasicForm(Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            ddate = Request.POST['d_date']

            ob1 = Request.POST['ob_field']
            repobj = Receiver.objects.get(pk=ob1)
            curobj = repobj

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

            rep = Tabel.objects.filter(date=ddate, obj=repobj).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

            for i in rep:                
                print(i)

            # теперь надо сформировать таблицу для вывода по подразделениям, отфильтровав по объекту

            for d in divis:
                #пробегаюсь по rep, смотрю есть ли записи с объектом o
                f=0
                d_kl=0

                for r in rep:
                    if d.pk==int(r['div']):
                        f=1 # нашли запись
                        
                        if r['kol__sum'] is None:
                            kk = 0
                        else:
                            kk = float(r['kol__sum'])

                        d_kl+=kk
                        # добавляем в массив
                        st = {
                            'Sotr': r['sotr__name'],
                            'div': d.pk,
                            'kol': kk,
                        }
                        smas.append(st)

                if f == 1: # Добавляем запись в массив подразделений
                    rec={
                        'divis': d,
                        'kol': d_kl,
                    }

                    dmas.append(rec)
            
            #  Формируем таблицу по не открытым чек листам за этот день
            cmas = []; n = 1; clist = ChList.objects.filter(obj=repobj) # Список чек листов по данному объекту
            
            for c in clist:
                r = ChListRecCreated ( ddate, c )
                if len(r) == 0:
                    cmas.append ({ 'chl': c, 'number': n, })
                    n = n + 1

            # Делаем отчет невыполненным заданиям по чек листам
            # сначала делаем список, чек листов, которые открыты по данному объекту
            for c in clist:
                r = ChListRecCreated ( ddate, c )
                if len(r) > 0:
                    omas.append(c)

            # формируем массив несделанных записей
            rmas = []
            ormas = []

            for n in omas:
                
                # формируем список записей по чек листам за этот день по данному объекту по данному чек листу
                rep = ChListTask.objects.filter(date=ddate, obj=repobj, chl=n)
                fl = 0

                # проверяем несделанные записи и записываем их в массив этих записей
                for w in rep:

                    s = ''

                    if w.chl.u1 is not None:
                        if len (str (w.chl.u1)) > 0:
                            if w.f1 != True:
                            # запись не выполнена, указываем участок 1
                                s = s + '(' + str (w.chl.u1) + ')'

                    if w.chl.u2 is not None:
                        if len (str (w.chl.u2)) > 0:
                            if w.f2 != True:
                            # запись не выполнена, указываем участок 2
                                s = s + '(' + str (w.chl.u2) + ')'

                    if w.chl.u3 is not None:
                        if len (str (w.chl.u3)) > 0:
                            if w.f3 != True:
                            # запись не выполнена, указываем участок 3
                                s = s + '(' + str (w.chl.u3) + ')'

                    if len (s) > 0:
                        #  добавляем в массив
                        rec = { 
                            'task': w,
                            'remark': s,
                        }
                            
                        rmas.append(rec)
                        fl = 1
                
                if fl == 1:
                    ormas.append(n)

            ocmas = []
            cnmas = []
            # делаем отчет по проконтролированным записям в чек листах которые не приняты контролем
            # делаем это по списку открытых чек листов (omas)

            for n in omas:
                
                # формируем список записей по чек листам за этот день по данному объекту по данному чек листу
                rep = ChListTask.objects.filter(date=ddate, obj=repobj, chl=n)
                fl = 0

                # проверяем несделанные записи и записываем их в массив этих записей
                for w in rep:

                    if w.chl.u1 is not None:
                        if len (str (w.chl.u1)) > 0:
                            if w.cst1 != True:
                                # запись выполнена c проблемой, указываем участок 1, необходимо вставить запись с данными
                                if w.s1 is not None:
                                    otm = str (str (w.s1.name) + ',' + f'{w.t1.astimezone():%Y-%m-%d, %H:%M}')
                                else:
                                    otm = ''

                                rec = {
                                    'task': w,
                                    'uch': str (w.chl.u1),
                                    'otm': otm,
                                    'prov': str (str (w.cs1.name) + ',' + f'{w.ct1.astimezone():%Y-%m-%d, %H:%M}'),
                                    #'prov': str (str ('') + ',' + f'{w.ct1.astimezone():%Y-%m-%d, %H:%M}'),
                                    'rem': str (w.rem1),
                                }
                                cnmas.append(rec)
                                fl = 1                                

                    if w.chl.u2 is not None:
                        if len (str (w.chl.u2)) > 0:
                            if w.cst2 != True:
                                # запись выполнена c проблемой, указываем участок 2, необходимо вставить запись с данными
                                if w.s2 is not None:
                                    otm = str (str (w.s2.name) + ',' + f'{w.t2.astimezone():%Y-%m-%d, %H:%M}')
                                else:
                                    otm = ''

                                rec = {
                                    'task': w,
                                    'uch': str (w.chl.u2),
                                    'otm': otm,
                                    'prov': str (str (w.cs2.name) + ',' + f'{w.ct2.astimezone():%Y-%m-%d, %H:%M}'),
                                    #'prov': str (str ('') + ',' + f'{w.ct2.astimezone():%Y-%m-%d, %H:%M}'),
                                    'rem': str (w.rem2),
                                }
                                cnmas.append(rec)
                                fl = 1                                

                    if w.chl.u3 is not None:
                        if len (str (w.chl.u3)) > 0:
                            if w.cst3 != True:
                                # запись выполнена c проблемой, указываем участок 3, необходимо вставить запись с данными
                                if w.s3 is not None:
                                    otm = str (str (w.s3.name) + ',' + f'{w.t3.astimezone():%Y-%m-%d, %H:%M}')
                                else:
                                    otm = ''

                                rec = {
                                    'task': w,
                                    'uch': str (w.chl.u3),
                                    'otm': otm,
                                    'prov': str (str (w.cs3.name) + ',' + f'{w.ct3.astimezone():%Y-%m-%d, %H:%M}'),
                                    #'prov': str (str ('') + ',' + f'{w.ct3.astimezone():%Y-%m-%d, %H:%M}'),
                                    'rem': str (w.rem3),
                                }
                                cnmas.append(rec)
                                fl = 1                                
                
                if fl == 1:
                    ocmas.append(n)

            # Вывожу данные по выполнению по чек листам:
            # for s in omas:
            #     # делаю запрос по дате и текущему Ч/Л и объекту
            #     Chl = ChListTask.objects.filter(date=ddate, obj=repobj, chl=c)
            #     for n in stmas:
            #         # пробегаюсь по сотрудникам, и записям в чек листах за эту дату и фиксирую, кто отметил из сотрудников
            #         m = []
            #         for c in Chl:
                        
            #             if (c.s1 == s or c.s2 == s or c.s3 == s):

            #                 if len (str (c.chl.u1)) > 0:
            #                     if c.f1:
            #                         # Выполнено, надо добавить словарь с данными по строке
            #                         st = {                                        
            #                                 'uch': str (c.chl.u1),
            #                                 't': f'{w.t1.astimezone():%d-%m-%Y, %H:%M}',
            #                                 'chl': c.chl,
            #                         } 
            #                         m.append (s)

            #                 if len (str (c.chl.u2)) > 0:
            #                     if c.f2:
            #                         # Выполнено, надо добавить словарь с данными по строке
            #                         s = {                                        
            #                                 'uch': str (c.chl.u2),
            #                                 't': f'{w.t2.astimezone():%d-%m-%Y, %H:%M}',
            #                                 'chl': c.chl,
            #                         }
            #                         m.append (s)

            #                 if len (str (c.chl.u3)) > 0:
            #                     if c.f2:
            #                         # Выполнено, надо добавить словарь с данными по строке
            #                         s = {                                        
            #                                 'uch': str (c.chl.u3),
            #                                 't': f'{w.t3.astimezone():%d-%m-%Y, %H:%M}',
            #                                 'chl': c.chl,
            #                         }
            #                         m.append (s)
                    
            #         # собрали все записи, который делал сотрудник с, теперь вставляю в массив для вывода
            #         if len (m) > 0: 
            #             k = 0

            srmas = [] # Список сотрудников с чек листам и отметками
            chltask = ChListTask.objects.filter(date=ddate, obj=repobj) # Делаем запрос по всем отметкам за этот день по данному объекту

            for s in stmas: # Перебираю сотрудников, которые принимали участие в отметке в чек листах                
                stm = [] # массив из отмеченных записей по сотруднику
                for c in omas: # перебираем открытые чек листы
                    cm = [] # массив из записей чек листов по сотруднику

                    for r in chltask:
                        #  делаю выборку из отмеченных записей
                        if (r.chl == c) & (r.s1 == s or r.s2 == s or r.s3 == s):

                            if len (str (r.chl.u1)) > 0:
                                if r.f1:
                                    # Выполнено, надо добавить словарь с данными по строке
                                    st = {                                        
                                             'uch': str (r.chl.u1),
                                             't': f'{r.t1.astimezone():%d-%m-%Y, %H:%M}',
                                             'task': r.chlrec.name,
                                    } 
                                    cm.append (st)

                            if len (str (r.chl.u2)) > 0:
                                 if r.f2:
                                    # Выполнено, надо добавить словарь с данными по строке
                                    st = {                                        
                                            'uch': str (r.chl.u2),
                                            't': f'{r.t2.astimezone():%d-%m-%Y, %H:%M}',
                                            'task': r.chlrec.name,
                                     }
                                    cm.append (st)

                            if len (str (r.chl.u3)) > 0:
                                 if r.f3:
                                    # Выполнено, надо добавить словарь с данными по строке
                                    st = {                                        
                                            'uch': str (r.chl.u3),
                                            't': f'{r.t3.astimezone():%d-%m-%Y, %H:%M}',
                                            'task': r.chlrec.name,
                                     }
                                    cm.append (st)
                    
                    if len (cm) > 0:
                        #  массив cm с отметками по чек листу готов, пакуем его в словарь с чек листами
                        st = {
                            'chl': c,
                            'tasks': cm,
                        }
                        
                        stm.append(st)
                
                if len (stm) > 0:
                    #  массив stm с чек листами с отметками по чек листу готов, пакуем его в словарь с сотрудниками
                    st = {
                        'sotr': s,
                        'vip': stm, #  выполнение
                    }

                    srmas.append(st)
            
            #  делаем выборку по полученной информации
            # for s in sr:
            #     print (s['sotr'].name)
            #     v = s['vip']
            #     for k in v:
            #         print ('   ' + k['chl'].name)
            #         t = k['tasks']
            #         for i in t:
            #             print ('     ' + i['uch'] + ':' + ' '+ i['t'] + '  ' + i['task'])

            # for s in srmas:
            #     print (s['sotr'].name)
            #     for k in s['vip']:
            #         print ('   ' + k['chl'].name)
            #         for i in k['tasks']:
            #             print ('     ' + i['uch'] + ':' + ' '+ i['t'] + '  ' + i['task'])

    else:
        formreport = ChlReportBasicForm()

    return render(Request, 'catalog/chlreportbasic.html', {'dmas': dmas, 'smas': smas, 'cmas': cmas, 'rmas': rmas, 
        'omas': ormas, 'ocmas': ocmas, 'cnmas': cnmas, 'srmas': srmas,
        'form': formreport, 'obj': obj, 'ob': curobj, 'user': Request.user, 
        'menu': mn, 'title': 'Отчет по Ч/Л основной.', 'ddate': ddate, 
        })

def ChlReportControl (Request):
    
    # отчет по конторолю
    usr = ''
    curobj = ''
    mas = [] # массив для записей с проблемами
    omas = [] # список объектов с данными для отображения

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 


    begindate = datetime.date.today()
    ddate1 = f'{begindate:%Y-%m-%d}'

    enddate = datetime.date.today()
    ddate2 = f'{enddate:%Y-%m-%d}'

    # Ищу проблемные задания, где не установлен флаг cst == true
    ts = ChListTask.objects.filter(date__range=[ddate1, ddate2], cst1=False).values

    objlist = Receiver.objects.all ()
    

    if Request.method == 'POST':
        
        formreport = ChlReportControlForm(Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            omas = []
            mas = []
            ddate1 = Request.POST['d_date1']
            ddate2 = Request.POST['d_date2']

            # date__range=[begindate, enddate] , (Q(cst1=False) | Q(cst2=False) | Q(cst3=False))
            # ищем все проблемные отметки
            ts = ChListTask.objects.filter(date__range=[ddate1, ddate2], cst1=False) | ChListTask.objects.filter(date__range=[ddate1, ddate2], cst2=False) | ChListTask.objects.filter(date__range=[ddate1, ddate2], cst3=False)

            # формирую массив со значениями
            for v in ts:

                print(v)
                # ищу картинку

                # ищу фото в коллекции
                img1 = ''; img2 = ''; img3 = ''
                im = UploadTaskImages.objects.filter(taskpk__pk=v.pk) 

                for j in im:
                    if j.unumber == 1:
                        img1 = j.img
                    elif j.unumber == 2:
                        img2 = j.img
                    elif j.unumber == 3:
                        img3 = j.img

                # готовии информацию по работающим сотрудникам
                st_info = SotrTabelInfo (v.date, v.obj, v.div)
                ss = ''

                for e in st_info:
                    ss += e['sotrdata']
                    ss += '<br/>'

                st_info = ss

                if v.chl.u1 is not None:
                    if len (str (v.chl.u1)) > 0:
                        if v.cst1 != True:
                            # print ('Участок 1: ' + str (v.chl.u1) )
                            # запись выполнена c проблемой, указываем участок 1, необходимо вставить запись с данными
                            # отметил ...
                            if v.s1 is not None:
                                #print('Отметил: ' + str (v.s1))
                                otm = str (str (v.s1.name) + ',' + f'{v.t1.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                otm = ''
                            # проконтролировал
                            if v.cs1 is not None:
                                #print ('Контроль: ' + str (v.cs1))
                                con = str (str (v.cs1.name) + ',' + f'{v.ct1.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                con = ''                            
                            
                            rec = {
                                    'task': v,
                                    'uch': str (v.chl.u1),
                                    'otm': otm,
                                    'con': con,
                                    'rem': str (v.rem1),
                                    'img': img1,
                                    'sotrdata': st_info,
                                }
                            mas.append(rec)                
                
                if v.chl.u2 is not None:
                    if len (str (v.chl.u2)) > 0:
                        if v.cst2 != True:
                            print ('Участок 2: ' + str (v.chl.u2) )
                            # запись выполнена c проблемой, указываем участок 2, необходимо вставить запись с данными
                            # отметил ...
                            if v.s2 is not None:
                                #print('Отметил: ' + str (v.s2))
                                otm = str (str (v.s2.name) + ',' + f'{v.t2.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                otm = ''
                            # проконтролировал
                            if v.cs2 is not None:
                                #print ('Контроль: ' + str (v.cs2))
                                con = str (str (v.cs2.name) + ',' + f'{v.ct2.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                con = ''                            
                            
                            rec = {
                                    'task': v,
                                    'uch': str (v.chl.u2),
                                    'otm': otm,
                                    'con': con,
                                    'rem': str (v.rem2),
                                    'img': img2,
                                    'sotrdata': st_info,
                                }
                            mas.append(rec)                
                
                if v.chl.u3 is not None:
                    if len (str (v.chl.u3)) > 0:
                        if v.cst3 != True:
                            #print ('Участок 3: ' + str (v.chl.u3) )
                            # запись выполнена c проблемой, указываем участок 3, необходимо вставить запись с данными
                            # отметил ...
                            if v.s3 is not None:
                                #print('Отметил: ' + str (v.s3))
                                otm = str (str (v.s3.name) + ',' + f'{v.t3.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                otm = ''
                            # проконтролировал
                            if v.cs3 is not None:
                                #print ('Контроль: ' + str (v.cs3))
                                con = str (str (v.cs1.name) + ',' + f'{v.ct1.astimezone():%Y-%m-%d, %H:%M}')
                            else:
                                con = ''                            
                            
                            rec = {
                                    'task': v,
                                    'uch': str (v.chl.u3),
                                    'otm': otm,
                                    'con': con,
                                    'rem': str (v.rem3),
                                    'img': img3,
                                    'sotrdata': st_info,
                                }
                            mas.append(rec) 
            
            if len(mas) > 0:
                # формируем данные по выводу с группировкой по объектам
                for i in objlist:
                    p = []

                    for v in mas:
                        if v['task'].obj == i:
                            # нашли запись, надо вставить в список по объекту
                            p.append(v)
                    
                    if len(p) > 0: 
                        #формируем словарь по объектам
                        rec = {
                            'obj': i,
                            'contdata': p,
                        }
                        omas.append(rec)


    else:
        formreport = ChlReportControlForm()

    return render(Request, 'catalog/chlreportcontrol.html', {'bdate': ddate1, 'edate': ddate2,  'user': Request.user, 
        'menu': mn, 'title': 'Отчет контроль по Ч/Л.', 'omas': omas,
        })
    

def KPITaskReport(Request):

    #Отчет KPI по выполненным задачам
    #Сотрудники, кол-во задач за период сортировано по количеству задач

    smas = [] # список сотрудников c с данными о выполнении
    cmas = [] # список сотрудников c с данными о контроле
    r_count = 0
    c_count = 0

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 


    begindate = datetime.date.today()
    ddate1 = f'{begindate:%Y-%m-%d}'

    enddate = datetime.date.today()
    ddate2 = f'{enddate:%Y-%m-%d}'

    sm = Sotr.objects.filter(active=True)
    #sm = Sotr.objects.filter(date__range=[ddate1, ddate2], cst1=False).values

    if Request.method == 'POST':
        
        formreport = KPITaskReportForm (Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            ddate1 = Request.POST['d_date1']
            ddate2 = Request.POST['d_date2']
            smas = []
            cmas = []
            r_count = 0
            c_count = 0

            begindate = ddate1
            enddate = ddate2

            # date__range=[begindate, enddate] , (Q(cst1=False) | Q(cst2=False) | Q(cst3=False))
            # ищем все проблемные отметки

            # Пробегаюсь по массиву сотрудников и заполняю массив со списками полученных данных
            for i in sm:
                
                r1 = ChListTask.objects.filter(date__range=[begindate, enddate], s1=i).count()
                r2 = ChListTask.objects.filter(date__range=[begindate, enddate], s2=i).count()
                r3 = ChListTask.objects.filter(date__range=[begindate, enddate], s3=i).count()

                c1 = ChListTask.objects.filter(date__range=[begindate, enddate], cs1=i).count()
                c2 = ChListTask.objects.filter(date__range=[begindate, enddate], cs2=i).count()
                c3 = ChListTask.objects.filter(date__range=[begindate, enddate], cs3=i).count()

                r = r1 + r2 + r3
                c = c1 + c2 + c3

                if r > 0:
                    # вставляем в массив словарь
                    st = {
                        'sotr': i,
                        'count': r,
                    }

                    smas.append(st)
                    r_count += r

                if c > 0:
                    # вставляем в массив словарь
                    st = {
                        'sotr': i,
                        'count': c,
                    }

                    cmas.append(st)
                    c_count += c
            
            # надо отсортировать наш массив по убыванию
            r = 0
            smas = sorted(smas, key=lambda x: x['count'], reverse=True)
            cmas = sorted(cmas, key=lambda x: x['count'], reverse=True)
                

    else:
        formreport = KPITaskReportForm ()

    return render(Request, 'catalog/kpitaskreport.html', {'bdate': ddate1, 'edate': ddate2,  'user': Request.user, 
            'menu': mn, 'title': 'Отчет KPI по от заданиям в Ч/Л.', 'smas': smas, 'cmas': cmas, 'r_count': r_count, 
            'c_count': c_count,
        })
