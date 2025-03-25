from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.http import HttpResponse

from .views import getmenu
from .models import Receiver, StopList, StopListRemark, MenuList, CauseList

import datetime
from json import loads

# Create your views here.
from .forms import StopListForm, AddStopListForm, AddStopListRemarkForm, StopListReportForm
from django.db.models import Q

from datetime import datetime, date, timedelta

def AddStopList(Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    sstr = '' # строка поиска

    
    obj = Request.user.OBJ # Первоначально Объект как у пользователя в настройках
    cauid = CauseList.objects.get(id=1) # по умолчанию причина = 1
    cauinfo = '' # по умолчанию пусто


    mlist = MenuList.objects.filter(obj=obj).order_by('name')  # Список меню сортированный по имени но отобранный по объекту
    # mlist = MenuList.objects.filter(obj=obj).order_by('name')

    objlist = Receiver.objects.all() # Список мест объектов (Ресторанов) / по умолчанию - тот, который в пользователе
    clist = CauseList.objects.all() # Список причин

    dt = datetime.today ()
    sldate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':

        formstoplist = AddStopListForm(Request.POST)
        if formstoplist.is_valid(): 
            
            # нажали кнопку создания записи стоп листа, необходимо ее обработать ))
            # и создать запись в заявке )))
            sd = Request.POST['sl_date']            
            
            obj = Request.POST['stl_object']
            cauid = Request.POST['cause_object']
            cauinfo = Request.POST['remark']

            searchstring = Request.POST['searchstring']
            # ищу объект по id
            obj = Receiver.objects.get(id=obj)
            cauid = CauseList.objects.get(id=cauid)

            # определяю, нажата ли клавиша поиск...
            ch = Request.POST['choise']

            if ch=='search':

                # нажата клавиша поиск, выполняем команду поиска, обновляем, ничего не создаем
                
                if searchstring != '':
                    # надо отфильтровать по строке
                    searchstring=searchstring.upper()
                    # list = MenuList.objects.filter(name__icontains=searchstring).order_by('name')  # Список меню фильтрую по строке
                    mlist = MenuList.objects.filter(name__icontains=searchstring,obj=obj).order_by('name')  # Список меню фильтрую по строке
                    sstr = searchstring
                else:
                    mlist = MenuList.objects.filter(obj=obj).order_by('name')

            if ch=='create':
                
                # надо создать, поэтому формирую список в зависимости от фильтра searchstring
                if searchstring != '':
                    # надо отфильтровать по строке
                    searchstring=searchstring.upper()
                    mlist = MenuList.objects.filter(name__icontains=searchstring, obj=obj).order_by('name')  # Список меню фильтрую по строке
                    sstr = searchstring
                else:
                    #mlist = MenuList.objects.filter(obj=obj).order_by('name')
                    mlist = MenuList.objects.filter(obj=obj).order_by('name')

                mas = []

                # надо найти как то  количество, которое я поставил ))
                for n in mlist:
                    st ='nomen' + str(n.id)
                    # проверяю, есть ли он в чек боксе
                    if Request.POST.get(st) == '':
                        # надо вставлять в массив
                            os = 'ost' + str(n.id)
                            ost = Request.POST.get(os)

                            rec = {
                                'nomen': n,
                                'ost': ost,
                            }                        
                            mas.append(rec)
                        
                # пора формировать запись в базе по стоп листу
                for i in mas:
                    # добавяю запись в таблицу стоп листа
                    n=i['nomen']

                    os = i['ost']
                    if os == '':
                        ost = 0
                    else:
                        ost = int (os)

                    tm=now()
                                                    
                    # надо проверить, есть ли он в стопе ?
                    l = StopList.objects.filter(menu=n, status=1)
                    if len (l) == 0:
                        s=StopList(datecreated=tm, status=1, 
                                   menu=n, cause=cauid, obj=n.obj, causeinfo = cauinfo, 
                                   autor=Request.user.sotr, ost = ost,
                                   date_exe=None)
                        s.save()
                        print(i['nomen'])
            
                #теперь надо перенаправить на страницу стоп листов
                if len(mas) > 0:                    
                    olist = [] # список объектов 
                    mlist = [] # список блюд в стопе, сгруппированный по объектам
                    rlist = [] # список комментариев в стопе
                    rmas = [] # результирующий массив с данными
                    mas = []

                    olist = Receiver.objects.all() # список обьектов
    
                    for n in olist:

                        mas = StopList.objects.filter(status=1, obj=n)  # отбираем по объекту, статусу
                        if len (mas) > 0:
                            #  создаем запись по объекту
                            m = []

                            for i in mas:
                                # собираем данные по стопам
                                st = {
                                    'menu': i.menu,
                                    'ost': i.ost,
                                    'dcreated': i.datecreated,
                                    'autor': i.autor.name,
                                    'cause': i.cause,
                                    'causeinfo': i.causeinfo,
                                    'pk': i.pk,
                                }
                                m.append(st)
            
                            st = {
                            'obj': n,
                            'objdata': m,
                            }

                            mlist.append(st)         
                    mn = getmenu(Request)

                    sdate = datetime.today()
                    sdate = f'{sdate:%Y-%m-%d}'
                    
                    SL = StopListForm()                
                    return render(Request, 'catalog/stoplistview.html', {'mlist': mlist, 'form': SL, 'sdate': sdate, 'loginuser': usr, 
                        'menu': mn, 'title': 'Стоп-лист.', 'rlist': rlist, })                    
                    
    else:    

        formstoplist = AddStopListForm()        

    return render(Request, 'catalog/addstoplist.html', {'mlist': mlist, 'form': formstoplist, 
            'loginuser': usr, 'menu': mn, 'title': 'Добавление в стоп-лист', 'objset': obj, 'causeset': cauid,
            'objlist': objlist, 'clist': clist, 'date_stoplist': sldate, 'mstr': sstr, 'rem': cauinfo,
            })

def AddStopListRemark(Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    sstr = '' # строка поиска

    
    obj = Request.user.OBJ # Первоначально Объект как у пользователя в настройках
    cauid = CauseList.objects.get(id=1) # по умолчанию причина = 1
    cauinfo = '' # по умолчанию пусто


    mlist = MenuList.objects.filter(obj=obj).order_by('name')  # Список меню сортированный по имени но отобранный по объекту
    # mlist = MenuList.objects.filter(obj=obj).order_by('name')

    objlist = Receiver.objects.all() # Список мест объектов (Ресторанов) / по умолчанию - тот, который в пользователе
    clist = CauseList.objects.all() # Список причин

    dt = datetime.date.today()
    sldate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':

        formstoplist = AddStopListRemarkForm(Request.POST)
        if formstoplist.is_valid(): 
            
            # нажали кнопку создания записи стоп листа, необходимо ее обработать ))
            # и создать запись в заявке )))
            sd = Request.POST['sl_date']            
            
            obj = Request.POST['stl_object']
            cauid = Request.POST['cause_object']
            textremark = Request.POST['textremark']

            searchstring = Request.POST['searchstring']
            # ищу объект по id
            obj = Receiver.objects.get(id=obj)
            cauid = CauseList.objects.get(id=cauid)

            tm = now()

            # определяю, нажата ли клавиша поиск...
            ch = Request.POST['choise']

            if ch=='create':
                
                s=StopListRemark (datecreated=tm, status=1, 
                                   menu=n, cause=cauid, obj=n.obj, causeinfo = '', remark = textremark,
                                   autor=Request.user.sotr, ost = ost,
                                   date_exe=None)
                s.save()
            
                #теперь надо перенаправить на страницу стоп листов,  заполняем  данные
                olist = [] # список объектов 
                mlist = [] # список блюд в стопе, сгруппированный по объектам
                rlist = [] # список комментариев в стопе
                rmas = [] # результирующий массив с данными
                mas = []

                olist = Receiver.objects.all() # список обьектов
    
                for n in olist:

                    mas = StopList.objects.filter(status=1, obj=n)  # отбираем по объекту, статусу
                    if len (mas) > 0:
                        #  создаем запись по объекту
                        m = []

                        for i in mas:
                                # собираем данные по стопам
                            st = {
                                    'menu': i.menu,
                                    'ost': i.ost,
                                    'dcreated': i.datecreated,
                                    'autor': i.autor.name,
                                    'cause': i.cause,
                                    'causeinfo': i.causeinfo,
                                    'pk': i.pk,
                                }
                            m.append(st)
            
                        st = {
                            'obj': n,
                            'objdata': m,
                            }

                        mlist.append(st)         
                mn = getmenu(Request)

                sdate = datetime.date.today()
                sdate = f'{sdate:%Y-%m-%d}'
                    
                SL = StopListForm()                
                return render(Request, 'catalog/stoplistview.html', {'mlist': mlist, 'form': SL, 'sdate': sdate, 'loginuser': usr, 
                        'menu': mn, 'title': 'Стоп-лист.', 'rlist': rlist, })                    
                    
    else:    

        formstoplist = AddStopListForm()        

    return render(Request, 'catalog/addstoplistremark.html', {'mlist': mlist, 'form': formstoplist, 
            'loginuser': usr, 'menu': mn, 'title': 'Добавление в стоп-лист', 'objset': obj, 'causeset': cauid,
            'objlist': objlist, 'clist': clist, 'date_stoplist': sldate, 'mstr': sstr, 'rem': cauinfo,
            })


def StopListView(Request):

    # вывожу список по стопам

    usr = ''
    mn = getmenu(Request)

    sdate = datetime.today()
    sdate = f'{sdate:%Y-%m-%d}'

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    olist = [] # список объектов 
    mlist = [] # список блюд в стопе, сгруппированный по объектам
    rlist = [] # список комментариев в стопе
    rmas = [] # результирующий массив с данными
    mas = []

    olist = Receiver.objects.all() # список обьектов
    
    for n in olist:

        mas = StopList.objects.filter(status=1, obj=n)  # отбираем по объекту, статусу
        if len (mas) > 0:
            #  создаем запись по объекту
            m = []

            for i in mas:
                # собираем данные по стопам
                st = {
                    'menu': i.menu,
                    'ost': i.ost,
                    'dcreated': i.datecreated,
                    'autor': i.autor.name,
                    'cause': i.cause,
                    'causeinfo': i.causeinfo,
                    'pk': i.pk,
                }
                m.append(st)
            
            st = {
                'obj': n,
                'objdata': m,
            }

            mlist.append(st)         

    if Request.method == 'POST':

        SL = StopListForm(Request.POST)

        if SL.is_valid(): 
            k=0
        
    
    SL = StopListForm()                

    return render(Request, 'catalog/stoplistview.html', {'mlist': mlist, 'form': SL, 'sdate': sdate, 'loginuser': usr, 
                        'menu': mn, 'title': 'Стоп-лист.', 'rlist': rlist, })


def StopListRecDel (Request, slrec):

    # Бомбим нажатие по кнопке удалить из стоп листа
    
    l = len(slrec)
    if l > 0:
        pk=int(slrec)
    else:
        pk=0

    # убираем из списка по флагу
    StopList.objects.filter(pk=pk).update(status=0, autor_exe=Request.user.sotr, date_exe=datetime.now())

    return render (Request, 'catalog/accessdenied.html', {'title': 'Убрали из стопа ...'})

def StopListReport (Request):
    
    # делаем отчет по стоп листу за период с начала месяца по текущую дату
    usr = ''

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    # Всем пользователям доступен этот отчет
    # if Request.user.A_Tabel != True:
    #     # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
    #     return redirect('AccessDenied') 

    cmas = CauseList.objects.all()
    omas = Receiver.objects.all()
    nmas = MenuList.objects.all()

    begindate = date.today()
    enddate = date.today()
    begindate.replace(day=1)

    td1 = timedelta(days=1)
    enddate += td1

    begindate = datetime (begindate.year, begindate.month, 1)
    enddate = datetime (enddate.year, enddate.month, enddate.day)
    
    objmas = []

    for j in omas: # пробегаемся по объектам:
        
        mas = [] # массив из словарей с данными по причинам

        for k in cmas: # пробегаемся по этой причине:

            #rep = StopList.objects.filter(date__range=[begindate, enddate], obj=j, cause=k) # ищем записи по этому объекту и этой причине
            rep = StopList.objects.filter(datecreated__range=[begindate, enddate], obj=j, cause=k) # ищем записи по этому объекту и этой причине
            cm = [] # массив номенклатуры по данной причине
            
            for n in nmas: # пробегаюсь по меню

                if n.obj == j: # номенклатура относится к данному объекту
                    
                    kol = 0 # количество стопов
                    tm = 0 #  количество времени (в часах)

                    # подсчитываем количество и время в стопе
                    for r in rep:
                        if r.menu == n: # нашли
                            kol += 1
                            #  определяю время
                            if r.date_exe is not None:
                                tm += round (((r.date_exe-r.datecreated).total_seconds() / 60 / 60), 2)
                            else:
                                tm += 12 # просто прибавляем 12 часов
                    
                    if kol != 0: # нашли, вставляем в массив
                        st = {
                            'menu': n,
                            'kol': kol,
                            'tm': round (tm, 2)
                        }
                        cm.append(st) # добавили номенклатуру в массив причин
            
            if len(cm)>0:

                # подсчитываю данные в причине и вставляю в массив по причине
                kol = 0
                tm = 0

                # сортируем по количеству
                cm1 = sorted(cm, key=lambda p: p['kol'], reverse=True)

                for t in cm1:
                    kol += t['kol']
                    tm += t['tm']

                st = {
                    'cause': k,
                    'kol': kol,
                    'tm': round (tm, 2),
                    'mas': cm1,
                }

                mas.append(st)

        if len(mas)>0: # вствляем в массив по объектам
            # подсчитываю данные
            kol = 0
            tm = 0

            # сортируем по количеству
            mas1 = sorted(mas, key=lambda p: p['kol'], reverse=True)

            for u in mas1:
                kol += u['kol']
                tm += u['tm']
            
            st = {
                'obj': j,
                'kol': kol,
                'tm': round (tm, 2),
                'mas': mas1,
                }

            objmas.append(st)

    # вывожу данные:
    for i in objmas:
        print (str(i['obj']) + ' ' + str (i['kol']) + '  ' + str (i['tm']))

        for j in i['mas']:
            print ('    ' + str(j['cause']) + ' ' + str (j['kol']) + '  ' + str (j['tm']))

            for k in j['mas']:
                print ('        ' + str(k['menu']) + ' ' + str (k['kol']) + '  ' + str (k['tm']))


    if Request.method == 'POST':
        
        formreport = StopListReportForm (Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            begindate = datetime.strptime(begindate, '%Y-%m-%d')
            enddate = datetime.strptime(enddate, '%Y-%m-%d')

            objmas = []

            for j in omas: # пробегаемся по объектам:
        
                mas = [] # массив из словарей с данными по причинам

                for k in cmas: # пробегаемся по этой причине:

                    #rep = StopList.objects.filter(date__range=[begindate, enddate], obj=j, cause=k) # ищем записи по этому объекту и этой причине
                    rep = StopList.objects.filter(datecreated__range=[begindate, enddate], obj=j, cause=k) # ищем записи по этому объекту и этой причине
                    cm = [] # массив номенклатуры по данной причине
            
                    for n in nmas: # пробегаюсь по меню

                        if n.obj == j: # номенклатура относится к данному объекту
                    
                            kol = 0 # количество стопов
                            tm = 0 #  количество времени (в часах)

                            # подсчитываем количество и время в стопе
                            for r in rep:
                                if r.menu == n: # нашли
                                    kol += 1
                                    #  определяю время
                                    if r.date_exe is not None:
                                        tm += round ((r.date_exe-r.datecreated).total_seconds() / 60 / 60, 2)
                                    else:
                                        tm += 12 # просто прибавляем 12 часов
                    
                            if kol != 0: # нашли, вставляем в массив
                                st = {
                                    'menu': n,
                                    'kol': kol,
                                    'tm': round (tm, 2),
                                }
                                cm.append(st) # добавили номенклатуру в массив причин
            
                    if len(cm)>0:

                        # подсчитываю данные в причине и вставляю в массив по причине
                        kol = 0
                        tm = 0

                        # сортируем по количеству
                        cm1 = sorted(cm, key=lambda p: p['kol'], reverse=True)

                        for t in cm1:
                            kol += t['kol']
                            tm += t['tm']

                        st = {
                            'cause': k,
                            'kol': kol,
                            'tm': round (tm, 2),
                            'mas': cm1,
                        }

                        mas.append(st)

                if len(mas)>0: # вствляем в массив по объектам
                    # подсчитываю данные
                    kol = 0
                    tm = 0

                    # сортируем по количеству
                    mas1 = sorted(mas, key=lambda p: p['kol'], reverse=True)

                    for u in mas1:
                        kol += u['kol']
                        tm += u['tm']
            
                    st = {
                        'obj': j,
                        'kol': kol,
                        'tm': round (tm, 2),
                        'mas': mas1,
                        }

                    objmas.append(st)

    else:
        
        formreport = StopListReportForm ()


    begindate = f'{begindate:%Y-%m-%d}'
    enddate = f'{enddate:%Y-%m-%d}'

    return render(Request, 'catalog/stoplistreport.html', { 'form': formreport, 'omas': objmas, 'user': Request.user, 
        'menu': mn, 'title': 'Отчет по STOP...ам.', 
        'begindate': begindate, 'enddate': enddate, 
        })


