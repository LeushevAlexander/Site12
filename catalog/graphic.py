from django.shortcuts import redirect, render
from .views import getmenu
from django.db.models import Q

from .models import Sotr, Podrazd, Position, Receiver, Graphic
from .forms import AddGraphicForm, GraphicForm
import datetime
import locale
from django.utils.timezone import now
import json
from django.http import JsonResponse

locale.setlocale(locale.LC_ALL, "")

def AddGraphic (Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    usr = Request.user
    sstr = '' # строка поиска    
    
    slist = Sotr.objects.filter(active=True).order_by('name')  # Список сотрудников сортированный по имени но отобранный по активности
    objlist = Receiver.objects.all() # Список мест объектов производства (Ресторанов) / по умолчанию - тот, который в пользователе
    divlist = Podrazd.objects.all() # Список подразделений (Бар, Кухня и тд) / по умолчанию - тот, который в пользователе
    poslist = Position.objects.all() #Список позиций в графике

    obj = 0; div = 0; objid = 0; divid = 0; cobj = 0; cdiv = 0

    pmas = []
    st = {'name': '-', 'id': 0}
    pmas.append (st)
    for i in poslist:
        st={'name': i.name, 'id': i.pk}
        pmas.append (st)

    omas = []
    st = {'name': '[Все]', 'id': 0}
    omas.append (st)
    for i in objlist:
        st={'name': i.name, 'id': i.pk}
        omas.append (st)

    comas = []   # Массив для создания записей в  графике
    for i in objlist:
        st={'name': i.name, 'id': i.pk}
        comas.append (st)


    dmas = []
    st = {'name': '[Все]', 'id': 0}
    dmas.append (st)
    for i in divlist:
        st={'name': i.name, 'id': i.pk}
        dmas.append (st)

    cdmas = []
    for i in divlist:
        st={'name': i.name, 'id': i.pk}
        if i.pk != 3:
            cdmas.append (st)
    
    dt = datetime.date.today()
    gdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':

        formgraphic = AddGraphicForm(Request.POST)
        if formgraphic.is_valid(): 
            
            # нажали кнопку создания записи стоп листа, необходимо ее обработать ))
            # и создать запись в заявке )))
            gd = Request.POST['g_date']
            gdate = datetime.datetime.strptime(gd, '%Y-%m-%d')
            
            # Это данные для поиска

            gdate = f'{dt:%Y-%m-%d}'

            searchstring = Request.POST['searchstring']
            # ищу объект по id

            # Данные для создания
            cobjid = Request.POST['cg_object']
            cdivid = Request.POST['cdiv_object']

            cobjid = int(cobjid)
            cdivid = int(cdivid)

            if cobjid != 0:
                cobj = Receiver.objects.get(pk=cobjid)
            else:
                cobj = 0

            if cdivid != 0:
                cdiv = Podrazd.objects.get(pk=cdivid)
            else:
                cdiv = 0                    

            # определяю, нажата ли клавиша поиск...
            ch = Request.POST['choise']

            if ch=='search':

                gd = Request.POST['g_date']
                gdate = gd

                # нажата клавиша поиск, выполняем команду поиска, обновляем, ничего не создаем                
                if searchstring != '':
                    # надо отфильтровать по строке
                    slist = Sotr.objects.filter(name__iregex=searchstring,active=True).order_by('name')  # Список сотрудников фильтрую по строке без учета регистра


            if ch=='create':
                
                # надо создать записи в графике, поэтому формирую список в зависимости от фильтра searchstring
                # формируем общий список всех активных сотрудников
                slist = Sotr.objects.filter(active=True)
                mas = []
                gd = Request.POST['g_date']
                gdate = datetime.datetime.strptime(gd, '%Y-%m-%d')

                for n in slist:
                    # Надо проверить, есть ли сотрудник такой на странице
                    st ='sotr' + str(n.id)
                    if st in Request.POST: 

                        st ='sotr' + str(n.id)
                        kol = Request.POST[st]
                        kol = kol.replace(',', '.')

                        t1 = 'sotr_t1' + str(n.id)
                        t2 = 'sotr_t2' + str(n.id)
                        t1 = Request.POST[t1]
                        t2 = Request.POST[t2]

                        # позиция, на которой работает сотрудник
                        pos = 'pos_' + str(n.id)

                        if pos in Request.POST:
                            # позиция определена
                            pos = Request.POST[pos]
                            pos = int(pos)
                            if pos != 0:
                                pos = Position.objects.get(pk=pos)
                            else:
                                pos = ''
                        else:
                            pos = ''

                        if len(kol) > 0:
                            # Надо добавлять в список графика на дату                            
                            st = {
                            'sotr': n,
                            'kol': kol,
                            't1': t1,
                            't2': t2,
                            'pos': pos,
                            'sum': round (float(kol) * n.stavka, 2)
                            }                        
                        
                            mas.append(st)

                # вставляю записи графика из массива в базу
                for n in mas:
                    s = Graphic (datecreated=now(), status=True, date=gdate, obj=cobj, div=cdiv, pos=n['pos'],
                       sotr=n['sotr'], t1=n['t1'], t2=n['t2'], kol=n['kol'], sum=n['sum'], autor=usr.username)
                    s.save()
                
                #теперь надо перенаправить на страницу сообщения о создании записи по позициям
                #if len(mas) > 0:
                #    return render(Request, 'catalog/graphiccreated.html', {'slist': mas, 'loginuser': usr, 
                #    'menu': mn, 'title': 'График добавлен.', 'gdate': gd, 'obj': cobj, 'div': cdiv })
                begindate = datetime.date.today()
                ddate1 = f'{begindate:%Y-%m-%d}'

                enddate = begindate + datetime.timedelta(days=7)
                ddate2 = f'{enddate:%Y-%m-%d}'

                # подготавливаем для заполнения форму
                # для начала просто массив
                d = begindate

                mas = []

                # заполняем массив с данными по графику
                while d <= enddate:
        
                    # делаем выборку в таблице графика
                    g = Graphic.objects.filter(date = d, status=True)

                    st = {
                        'date': f'{d:%d-%m-%Y}',
                        }

                    mas.append(st)
                    d += datetime.timedelta(days=1)

                gform = GraphicForm ()
                
                return render(Request, 'catalog/graphicview.html', {'bdate': ddate1, 'edate': ddate2,  'user': Request.user, 
                    'menu': mn, 'title': 'График сотрудников', 'form': gform, 'dmas': mas, 'rmas': '',
                        })                
                    
    else:    
        formgraphic = AddGraphicForm()        

    return render(Request, 'catalog/addgraphic.html', {'slist': slist, 'form': formgraphic, 'sstr': sstr, 'gdate': gdate,
        'loginuser': usr, 'menu': mn, 'title': 'Добавление в график', 'objlist': omas, 'divlist': dmas, 'objset': obj, 'divset': div, 'mstr': sstr, 
        'cobjlist': comas, 'cdivlist': cdmas, 'cobjset': cobj, 'cdivset': cdiv, 'plist': pmas,
        })

def GraphicView (Request):
    
    # выводим график
    usr = ''
    mas = [] # массив данных для вывода графика
    rep = []
    srep = []
    G_edit = False
    G_admin = False

    sfid = 0 # id сотрудника для фильтра

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_Graphic:  #  Просматриваем общуу таблицу и кнопки создания/удаления
        G_edit = True
        G_admin = True

    if Request.user.A_TabelReportAdmin:  # Просматриваем только общую таблицу
        G_admin = True

    G_admin = True

    poslist = Position.objects.all() #Список позиций в графике

    pmas = []
    st = {'name': '-', 'id': 0}
    pmas.append (st)
    for i in poslist:
        st={'name': i.name, 'id': i.pk}
        pmas.append (st)
    
    #sotrlist = Sotr.objects.filter(active=True).order_by('name')
    if G_admin or G_edit:
        sotrlist = Sotr.objects.filter(active=True).order_by('name')
        objlist = Receiver.objects.all() # Список мест объектов производства (Ресторанов) / по умолчанию - тот, который в пользователе
        divlist = Podrazd.objects.exclude(pk=3) # Список подразделений, кроме администрации (Бар, Кухня и тд) / по умолчанию - тот, который в пользователе
    else:
        sotrlist = Sotr.objects.filter(active=True, pk=Request.user.sotr.pk).order_by('name') # Отбор только по текущему сотруднику
        divlist = Podrazd.objects.filter(pk=Request.user.sotr.div.pk) # Список подразделений, только свой) / по умолчанию - тот, который в пользователе
        objlist = Receiver.objects.filter(pk=Request.user.sotr.obj.pk) # Список мест объектов производства (Ресторанов) / по умолчанию - тот, который в пользователе

    begindate = datetime.date.today()
    ddate1 = f'{begindate:%Y-%m-%d}'

    enddate = begindate + datetime.timedelta(days=7)
    ddate2 = f'{enddate:%Y-%m-%d}'

    begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(ddate2, '%Y-%m-%d')

    if Request.method == 'POST':
        gform = GraphicForm (Request.POST)
        
        if gform.is_valid(): 

            # заполняем данные из формы
            ddate1 = Request.POST['d_date1']
            ddate2 = Request.POST['d_date2']
            #sf = Request.POST['sfilter_id']
            sfid = 0

            if sfid != 0:
                                               
                # Включаем фильтр по сотрудникам, id которого sfid
                sotrlist = Sotr.objects.filter(active=True, pk=sfid).order_by('name') # Отбор только по сотруднику
                # for i in sotrlist:
                #     divlist = Podrazd.objects.filter(pk=i.div.pk) # Список подразделений, только свой) / по умолчанию - тот, который в пользователе
                #     objlist = Receiver.objects.filter(pk=i.obj.pk) # Список мест объектов производства (Ресторанов) / по умолчанию - тот, который в пользователе


            # заполняем массив
            begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')
            enddate = datetime.datetime.strptime(ddate2, '%Y-%m-%d')
        else:
            gform = GraphicForm (Request.POST)
    else:
        gform = GraphicForm (Request.POST)

    d = begindate

    # заполняем массив с данными по графику
    while d <= enddate:
        
        # делаем выборку в таблице графика
        # g = Graphic.objects.filter(date = d, status=True)


        st = {
            'date': f'{d:%d-%m-%Y}',
            }

        mas.append(st)
        d += datetime.timedelta(days=1)        


    if 1 == 1:
        
        # Просто выполняем
        #gform = GraphicForm (Request.POST)
        
        if 1 == 1: 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            mas = []
            smas = []

            #ddate1 = Request.POST['d_date1']
            #ddate2 = Request.POST['d_date2']

            # заполняем массив
            #begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')
            #enddate = datetime.datetime.strptime(ddate2, '%Y-%m-%d')
            d = begindate

            while d <= enddate:
        
                # делаем выборку в таблице графика
                m = []
                g = Graphic.objects.filter(date = d, status=True)
                for v in g:
                    # делаем информацию по сотрудникам и графику
                    r = {
                        'sotr': v.sotr.name,
                        'dt': v.date,
                        't1': v.t1,
                        't2': v.t2,
                        'pos': v.pos.name,
                        'kol': v.kol,
                        'gpk': v.pk,
                        'obj': v.obj,
                        'div': v.div,
                        'pers': v.sotr,
                        'pos_pk': v.pos.pk,
                    }
                    m.append(r)

                st = {
                    'date': d.strftime('%d %b'),
                    'day': d.strftime('%a'),
                    'dn': int (d.strftime('%w')),
                    'sotrdata': m,
                    }

                mas.append(st)
                d += datetime.timedelta(days=1)

            #   Ищем сотрудников в массиве графика за этот период    
            rp = Graphic.objects.filter(date__range=[begindate, enddate], status=True)
                
            for l in sotrlist:                
                for u in rp:
                    if l == u.sotr:
                        # проверяем, есть ли он в массиве
                        if l not in smas:
                            smas.append(l)
                            break
                        

            datamas=[]  # массив дат
            d = begindate
            while d <= enddate:                    
                st = {
                        'dt': d,
                    }
                datamas.append(st)
                d += datetime.timedelta(days=1)                
            
            srep = [] # Список словарей для вывода по сотрудникам

            # теперь формируем группирование по сотрудникам
            for q in smas:

                sdmas = []  # массив за дни по сотруднику
                sot_kol = 0 # кол-во часов по сотруднику
                sot_sm = 0 # кол-во смен по сотруднику
                
                for i in datamas: # пробегаюсь по датам                
                    
                    dm = [] # список найденных записей по сотруднику за день

                    for l in rp:  # пробегаюсь по всем записям в графике
                        
                        if i['dt'].date () == l.date and l.sotr == q:
                            # нашли, заполняем строку
                            st = l.obj.name + ', ' + l.div.name + ' ' + l.t1 + '-' + l.t2 + ' ' + l.pos.name
                            kl = l.kol

                            rec = {
                                'info': st,
                                'kol': kl,                                
                                'dt': i['dt'],
                                'pos': l.pos.pk,
                            }

                            dm.append(rec)
                            
                            sot_kol += kl
                            sot_sm += 1
                        
                    if len(dm) == 0: # ничего не нашли за эту дату,  пустую запись вставляем
                        rec = {
                                'info': '',
                                'kol': 0,
                                'dt': i['dt'],
                                'pos': 0,
                            }

                        dm.append(rec)
                        
                    rec = {
                        'sd': dm,
                    }

                    st = ''
                    for r in dm:
                        st += r['info']; 
                        if len (dm) > 0:
                            st += '\n\r'

                    rec = {
                        'info': st,
                    }

                    sdmas.append(rec)



                rec = {
                    'sotr': q,
                    'sotrdata': sdmas,
                    'kol': sot_kol,
                    'sm': sot_sm,
                }

                srep.append(rec)

            # теперЬ формируем группировние дней с сотрудниками по объектам, подразделениям.
            # все находится в списке rep
            rep = []

            for q in objlist:
                
                obj_name = q.name
                obj_list = []

                for z in divlist:

                    div_name = z.name
                    div_list = []

                    # просматриваваем все списки по данному обхекту и подразделению
                    for j in mas:

                        for h in j['sotrdata']:
                            if h['div'] == z and h['obj'] == q: # подходит
                                div_list.append(h)

                    st = {
                        'div_name': div_name,
                        'div_list': div_list,
                    }

                    obj_list.append (st)
                
                st = {
                    'obj_name': obj_name,
                    'obj_list': obj_list,
                }

                rep.append (st) # Все находится в списке rep

            # теперь надо сформировать таблицу для вывода по дням
            # все делаем в таблице rep

            for i in rep: #  разворачиваем список объектов
                
                datamas = []

                d = begindate
                while d <= enddate:                    
                    st = {
                        'dt': d,
                        'kol': '', # количество часов на объекте в этот день
                    }
                    datamas.append(st)
                    d += datetime.timedelta(days=1)
                
                i['mas'] = datamas


                for j in i['obj_list']: # разворачиваем список подразделений, который в rep
                    
                    datamas = []
                    d = begindate
                    while d <= enddate:                    
                        st = {
                            'dt': d,
                            'kol': '', # количество часов в подразделении в этот день
                        }
                        datamas.append(st)
                        d += datetime.timedelta(days=1)
                
                    j['mas'] = datamas

                    q = j['div_list'] # список с данными о сотрудниках
                    gpk = [] # массив из сделанных записей, для контроля
                    sotrdata = [] # список с данными о сотрудниках

                    for a in range (10): # 10 строк с сотрудниками

                        datamas = []  #  формируем колонки
                        d = begindate
                        while d <= enddate:                    

                            # ищем запись сотрудника для отображения за эту дату
                            aa = ''; kl = 0; gg = 0; tt1 = ''; tt2 = ''; ddt = ''; ppos = ''; pos_pk = 0; obj_pk= 0; div_pk = 0

                            for t in j['div_list']:
                                if d.date () == t['dt']:                                    
                                    # надо проверить, есть ли идентификатор в массиве
                                    if t['gpk'] not in gpk:
                                        gpk.append(t['gpk'])
                                        # заполняем данные для отображения
                                        aa = t['sotr'] + ' (' + t['t1'] + '-' + t['t2'] + ') ' + t['pos']
                                        kl = t['kol']
                                        gg = t['gpk']    
                                        tt1 = t['t1']           
                                        tt2 = t['t2']        
                                        ddt = f'{d:%Y-%m-%d}'
                                        ppos = t['pos']
                                        pos_pk = t['pos_pk']
                                        obj_pk = t['obj'].pk
                                        div_pk = t['div'].pk
                                        break

                            st = {
                                    'dt': d,
                                    'kol': kl,
                                    'info': aa,
                                    'gpk': gg,
                                    'dd': d.strftime('%d %b'),
                                    't1': tt1,
                                    't2': tt2,
                                    'ddt': ddt,
                                    'pos': ppos,
                                    'pos_pk': pos_pk,
                                    'obj': obj_pk,
                                    'div': div_pk,
                                }
                            datamas.append(st)
                            d += datetime.timedelta(days=1)

                        st = {
                            'column': datamas,
                        }

                        # Проверяем на пустые строки
                        y = 0
                        for x in datamas:
                            if len (x['info']) > 0:
                                y = 1
                                break

                        if y != 0:
                            sotrdata.append(st)

                    j['sotrdata'] = sotrdata
            
            # подсчитываем количество часов в подразделениях
            for i in rep:
                for j in i['obj_list']: 
                    y = 0 

                    #  делаю выборку по дням
                    d = begindate
                    while d <= enddate:                    
                        kl = 0

                        for u in j['sotrdata']:
                            for t in u['column']:
                                if t['dt'] == d:
                                    kl += float (t['kol'])
                        
                        if kl != 0:
                            j['mas'][y]['kol'] = str (kl)

                        y += 1
                        d += datetime.timedelta(days=1)
            
            # подсчитываем количество часов в объектах
            for i in rep:                
                y = 0 
                
                #  делаю выборку по дням
                d = begindate
                while d <= enddate:                    
                    kl = 0

                    for j in i['obj_list']:
                        for u in j['mas']:
                            if u['dt'] == d:
                                if u['kol'] != '':
                                    kl += float (u['kol'])
                        
                    if kl != 0:
                            i['mas'][y]['kol'] = str (kl)

                    y += 1
                    d += datetime.timedelta(days=1)
    
    return render(Request, 'catalog/graphicview.html', {'bdate': ddate1, 'edate': ddate2,  'user': Request.user, 
        'menu': mn, 'title': 'График', 'form': gform, 'dmas': mas, 'rmas': rep, 'smas': srep, 'divmas': divlist, 'omas': objlist, 
        'G_edit': G_edit, 'G_admin': G_admin, 'pmas': pmas, 
        })

#Возврат json по запросу из приложения Bot
def GraphSotrInfo (Request, sid, d1, d2):

    mas = [] # возвращаемый массив дат    
    kol = 0
    sm = 0
    s = int (sid)
    sotr = Sotr.objects.get(pk=s)

    begindate = datetime.datetime.strptime(d1, '%Y-%m-%d').date()
    enddate = datetime.datetime.strptime(d2, '%Y-%m-%d').date()

    rep = Graphic.objects.filter(date__range=[begindate, enddate], status=True, sotr = sotr).order_by('date')

    d = begindate
    # заполняем массив с данными по графику
    while d <= enddate:

        st = ''

        for r in rep: # пробегаюсь по всем записям в графике
                        
            if r.date == d:
                # нашли, заполняем строку
                st = r.obj.name + ', ' + r.div.name + ' ' + r.t1 + '-' + r.t2 + ' ' + r.pos.name + '\r\n'
                kol += r.kol                
                sm += 1
        
        mas.append(st)
        d += datetime.timedelta(days=1)

    
    return JsonResponse({'sotr': sotr.name, 'sotrdata': mas, 'kol': kol, 'sm': sm, 'sotrid': sotr.pk })   


def GraphicRecDel (Request, gpk):
    # удаляем запись из графика (active ставим false)
    g = int (gpk)

    Graphic.objects.filter(pk=g).update(status=False)
    
    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def GraphicRecEdit (Request, gpk, dt, t1, t2, kol, pos, obj, div):

    # изменяем запись в графике (поля ставим, которые переданы)
    g = int (gpk)
    p = int (pos)
    d = int (div)
    o = int (obj)

    stavka = 0

    k = kol.replace(',', '.')
    k = float (k)

    a = Graphic.objects.filter(pk=g)

    for i in a:
        sotr = Sotr.objects.get(pk=i.sotr.pk)
        stavka = sotr.stavka        

    ss = k * stavka


    ddt = datetime.datetime.strptime(dt, '%Y-%m-%d')
    ddt = ddt.date()

    pp = Position.objects.get(pk=p)
    ob = Receiver.objects.get(pk=o)
    di = Podrazd.objects.get(pk=d)

    Graphic.objects.filter(pk=g).update(date=ddt, t1=t1, t2=t2, kol=k, pos=pp, obj = ob, div=di, sum=ss)
    
    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def GraphicRecCopy (Request, gpk, dt, t1, t2, kol, pos, obj, div):

    # изменяем запись в графике (поля ставим, которые переданы)
    g = int (gpk)
    p = int (pos)
    d = int (div)
    o = int (obj)

    stavka = 0

    k = kol.replace(',', '.')
    k = float (k)

    a = Graphic.objects.filter(pk=g)

    for i in a:
        sotr = Sotr.objects.get(pk=i.sotr.pk)
        stavka = sotr.stavka
        

    ss = k * stavka

    pp = Position.objects.get(pk=p)
    ob = Receiver.objects.get(pk=o)
    di = Podrazd.objects.get(pk=d)
    
    ddt = datetime.datetime.strptime(dt, '%Y-%m-%d')
    ddt = ddt.date()
    
    s = Graphic ( datecreated=now(), status=True, date=ddt, obj=ob, div=di, pos=pp,
                       sotr=sotr, t1=t1, t2=t2, kol=k, sum=ss, autor=Request.user.username )
    
    s.save()
    
    return render (Request, 'catalog/accessdenied.html', {'title': ''})
