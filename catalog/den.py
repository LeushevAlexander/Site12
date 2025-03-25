from django.shortcuts import redirect, render
from json import loads
from .views import getmenu
from django.db.models import Q
from .forms import DenForm
from .models import Receiver, Den
import datetime
from django.http import JsonResponse

def DenRecDel (Request, bpk):

    # удаляем запись из рабочих дней, физически
    b = int (bpk)

    Den.objects.filter(pk=b).delete ()
    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def GetF (st):

    val = 0

    if st == '':
        st = '0.0'

    st = st.replace(',', '.')
    val = float(st)

    return val

def DenRecEdit (Request):

    # считываем запись из банкетов 
    pk = int (loads(Request.body)['pk'])
    dt = datetime.datetime.strptime((loads(Request.body)['dt']), '%Y-%m-%d').date()
    objset = Receiver.objects.get(pk=int(loads(Request.body)['obj']))
    
    st = loads(Request.body)['vnal'] 
    vnal = GetF(st)

    st = loads(Request.body)['vbnal']
    vbnal = GetF(st)

    st = loads(Request.body)['vbs'] 
    vbs = GetF(st)

    st = loads(Request.body)['vpp'] 
    vpp = GetF(st)

    st = loads(Request.body)['vpr'] 
    vpr = GetF(st)

    st = loads(Request.body)['vsr'] 
    vsr = GetF(st)

    st = loads(Request.body)['vbar'] 
    vbar = GetF(st)

    st = loads(Request.body)['vkuh'] 
    vkuh = GetF(st)

    st = loads(Request.body)['chnal'] 
    chnal = GetF(st)

    st = loads(Request.body)['chbnal'] 
    chbnal = GetF(st)

    st = loads(Request.body)['kolg']
    kolg = GetF(st)

    st = loads(Request.body)['gorv'] 
    gorv = GetF(st)

    st = loads(Request.body)['gork'] 
    gork = GetF(st)

    st = loads(Request.body)['holv'] 
    holv = GetF(st)

    st = loads(Request.body)['holk'] 
    holk = GetF(st)

    st = loads(Request.body)['pizv'] 
    pizv = GetF(st)

    st = loads(Request.body)['pizk'] 
    pizk = GetF(st)

    st = loads(Request.body)['desv'] 
    desv = GetF(st)

    st = loads(Request.body)['desk'] 
    desk = GetF(st)

    st = loads(Request.body)['kofv'] 
    kofv = GetF(st)

    st = loads(Request.body)['kofk'] 
    kofk = GetF(st)

    st = loads(Request.body)['alkv'] 
    alkv = GetF(st)

    st = loads(Request.body)['alkk'] 
    alkk = GetF(st)

    # теперь изменяем данные в базе
    Den.objects.filter(pk=pk).update(date=dt, 
                                       obj=objset,
                                       vnal=vnal,
                                       vbnal=vbnal,
                                       vbc=vbs,
                                       vpp=vpp,
                                       vpr=vpr,
                                       vsert=vsr,
                                       vb=vbar,
                                       vk=vkuh,
                                       chn=chnal,
                                       chbn=chbnal,
                                       kolg=kolg,
                                       gorv=gorv,
                                       gork=gork,
                                       holv=holv,
                                       holk=holk,
                                       pizv=pizv,
                                       pizk=pizk,
                                       kofv=kofv,
                                       kofk=kofk,
                                       desv=desv,
                                       desk=desk,
                                       alkv=alkv,
                                       alkk=alkk,
                                    )    

    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def DenRecAdd (Request):

    # считываем запись из окна создания
    #pk = int (loads(Request.body)['pk'])

    dt = datetime.datetime.strptime((loads(Request.body)['dt']), '%Y-%m-%d').date()
    objset = Receiver.objects.get(pk=int(loads(Request.body)['obj']))
    
    st = loads(Request.body)['vnal'] 
    vnal = GetF(st)

    st = loads(Request.body)['vbnal']
    vbnal = GetF(st)

    st = loads(Request.body)['vbs'] 
    vbs = GetF(st)

    st = loads(Request.body)['vpp'] 
    vpp = GetF(st)

    st = loads(Request.body)['vpr'] 
    vpr = GetF(st)

    st = loads(Request.body)['vsr'] 
    vsr = GetF(st)

    st = loads(Request.body)['vbar'] 
    vbar = GetF(st)

    st = loads(Request.body)['vkuh'] 
    vkuh = GetF(st)

    st = loads(Request.body)['chnal'] 
    chnal = GetF(st)

    st = loads(Request.body)['chbnal'] 
    chbnal = GetF(st)

    st = loads(Request.body)['kolg']
    kolg = GetF(st)

    st = loads(Request.body)['gorv'] 
    gorv = GetF(st)

    st = loads(Request.body)['gork'] 
    gork = GetF(st)

    st = loads(Request.body)['holv'] 
    holv = GetF(st)

    st = loads(Request.body)['holk'] 
    holk = GetF(st)

    st = loads(Request.body)['pizv'] 
    pizv = GetF(st)

    st = loads(Request.body)['pizk'] 
    pizk = GetF(st)

    st = loads(Request.body)['desv'] 
    desv = GetF(st)

    st = loads(Request.body)['desk'] 
    desk = GetF(st)

    st = loads(Request.body)['kofv'] 
    kofv = GetF(st)

    st = loads(Request.body)['kofk'] 
    kofk = GetF(st)

    st = loads(Request.body)['alkv'] 
    alkv = GetF(st)

    st = loads(Request.body)['alkk'] 
    alkk = GetF(st)

    # теперь изменяем данные в базе
    B = Den (date=dt, 
                                        obj=objset,
                                       vnal=vnal,
                                       vbnal=vbnal,
                                       vbc=vbs,
                                       vpp=vpp,
                                       vpr=vpr,
                                       vsert=vsr,
                                       vb=vbar,
                                       vk=vkuh,
                                       chn=chnal,
                                       chbn=chbnal,
                                       kolg=kolg,
                                       gorv=gorv,
                                       gork=gork,
                                       holv=holv,
                                       holk=holk,
                                       pizv=pizv,
                                       pizk=pizk,
                                       kofv=kofv,
                                       kofk=kofk,
                                       desv=desv,
                                       desk=desk,
                                       alkv=alkv,
                                       alkk=alkk,
                                       autor=Request.user.sotr
                                    )  
    B.save()  

    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def DN (Num):

    s = '{0:,}'.format(Num).replace(',', ' ')
    return s

def GetVal (i):
    # Возвращает нормальное значение
    # если Null, то 0
    if i is None:
        v = 0
    else:
        v = i
    
    return v

def DenView (Request):
    
    
    # выводим рабрчие дни
    omas = [] # список объектов
    dmas = [] # список дней

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    omas = Receiver.objects.all()

    begindate = datetime.date.today()
    enddate = datetime.date.today()

    ddate1 = f'{begindate:%Y-%m-%d}'
    ddate2 = f'{enddate:%Y-%m-%d}'

    tdate = ddate1

    begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')

    b = Den.objects.filter(date__range=[ddate1, ddate2]).order_by('date')
    dmas = []; 

    for i in b:

        if i.autor is None: 
            au = '----'
        else:
            au = i.autor.name

        st = {
            'index': 0,
            'record': i,
            'dt': f'{i.date:%Y-%m-%d}',
            'vsego': DN (i.vnal + i.vbnal),
            'vnal1': DN (i.vnal),
            'vbnal1': DN (i.vbnal),
            'vnal': GetVal (i.vnal),
            'vbnal': GetVal (i.vbnal),
            'vbs': GetVal (i.vbc),
            'vpr': GetVal (i.vpr),
            'vpp': GetVal (i.vpp),
            'vsert': GetVal (i.vsert),
            'vbar': GetVal (i.vb),
            'vkuh': GetVal (i.vk),
            'chnal': GetVal (i.chn),
            'chbnal': GetVal (i.chbn),
            'kolg': GetVal (i.kolg),
            'gorv': GetVal (i.gorv),
            'gork': GetVal (i.gork),
            'holv': GetVal (i.holv),
            'holk': GetVal (i.holk),
            'pizv': GetVal (i.pizv),
            'pizk': GetVal (i.pizk),
            'desv': GetVal (i.desv),
            'desk': GetVal (i.desk),
            'alkv': GetVal (i.alkv),
            'alkk': GetVal (i.alkk),
            'kofv': GetVal (i.kofv),
            'kofk': GetVal (i.kofk),
            'autor': au,

        }

        dmas.append(st) 

    if Request.method == 'POST':
        dform = DenForm (Request.POST)
        
        if dform.is_valid(): 

            # заполняем данные из формы
            ddate1 = Request.POST['d_date1']
            ddate2 = Request.POST['d_date2']

            b = Den.objects.filter(date__range=[ddate1, ddate2]).order_by('date')

            dmas = []; 

            for i in b:
                if i.autor is None: 
                    au = '----'
                else:
                    au = i.autor.name

                st = {
                    'record': i,
                    'dt': f'{i.date:%Y-%m-%d}',
                    'vsego': DN (i.vnal + i.vbnal),
                    'vnal1': DN (i.vnal),
                    'vbnal1': DN (i.vbnal),
                    'vnal': GetVal (i.vnal),
                    'vbnal': GetVal (i.vbnal),
                    'vbs': GetVal (i.vbc),
                    'vpr': GetVal (i.vpr),
                    'vpp': GetVal (i.vpp),
                    'vsert': GetVal (i.vsert),
                    'vbar': GetVal (i.vb),
                    'vkuh': GetVal (i.vk),
                    'chnal': GetVal (i.chn),
                    'chbnal': GetVal (i.chbn),
                    'kolg': GetVal (i.kolg),
                    'gorv': GetVal (i.gorv),
                    'gork': GetVal (i.gork),
                    'holv': GetVal (i.holv),
                    'holk': GetVal (i.holk),
                    'pizv': GetVal (i.pizv),
                    'pizk': GetVal (i.pizk),
                    'desv': GetVal (i.desv),
                    'desk': GetVal (i.desk),
                    'alkv': GetVal (i.alkv),
                    'alkk': GetVal (i.alkk),
                    'kofv': GetVal (i.kofv),
                    'kofk': GetVal (i.kofk),
                    'autor': au,
                }

                dmas.append(st) 
        else:
            dform = DenForm (Request.POST)
    else:
        
        dform =DenForm ()

        b = Den.objects.filter(date__range=[ddate1, ddate2]).order_by('date')

        dmas = []; 

        for i in b:
                if i.autor is None: 
                    au = '----'
                else:
                    au = i.autor.name

                st = {
                    'record': i,                    
                    'vsego': DN (i.vnal + i.vbnal),
                    'vnal1': DN (i.vnal),
                    'vbnal1': DN (i.vbnal),
                    'dt': f'{i.date:%Y-%m-%d}',
                    'vnal': GetVal (i.vnal),
                    'vbnal': GetVal (i.vbnal),
                    'vbs': GetVal (i.vbc),
                    'vpr': GetVal (i.vpr),
                    'vpp': GetVal (i.vpp),
                    'vsert': GetVal (i.vsert),
                    'vbar': GetVal (i.vb),
                    'vkuh': GetVal (i.vk),
                    'chnal': GetVal (i.chn),
                    'chbnal': GetVal (i.chbn),
                    'kolg': GetVal (i.kolg),
                    'gorv': GetVal (i.gorv),
                    'gork': GetVal (i.gork),
                    'holv': GetVal (i.holv),
                    'holk': GetVal (i.holk),
                    'pizv': GetVal (i.pizv),
                    'pizk': GetVal (i.pizk),
                    'desv': GetVal (i.desv),
                    'desk': GetVal (i.desk),
                    'alkv': GetVal (i.alkv),
                    'alkk': GetVal (i.alkk),
                    'kofv': GetVal (i.kofv),
                    'kofk': GetVal (i.kofk),
                    'autor': au,
                }

                dmas.append(st)                 
        
    return render(Request, 'catalog/denview.html', {'bdate': ddate1, 'edate': ddate2, 'tdate': tdate, 'user': Request.user, 
        'menu': mn, 'title': 'Рабочие дни', 'form': dform, 'dmas': dmas, 'omas': omas, 
        })

def GetDPercent (all, pok):

    x = 0
    st = '%'

    if all != 0:
        x = pok / all * 100
        x = round (x, 2)

    if x != 0:
        st = str (x)
        st += '%'
    
    return st

def GetDRoundData (oid, bd, ed):

    id_obj = 0
    mas = []

    # возвращаем массив данных по графику круговой диаграммы
    if len(oid) != 0:
        id_obj = int (oid)

    else:
        id_obj = 0

    #  работаем уже с п подготовленными строками
    # ddate1 = f'{bd:%Y-%m-%d}'
    # ddate2 = f'{ed:%Y-%m-%d}'

    if id_obj == 0:
        rep = Den.objects.filter(date__range=[bd, ed]).order_by('date')
    else:
        ob = Receiver.objects.get(pk=id_obj)
        rep = Den.objects.filter(date__range=[bd, ed], obj = ob).order_by('date')

    # Считаем данные
    gorv = 0; holv = 0; pizv = 0; alkv = 0; desv = 0; kofv = 0; allv = 0
    gork = 0; holk = 0; pizk = 0; alkk = 0; desk = 0; kofk = 0; allk = 0

    for i in rep:
        gorv += i.gorv; gork += i.gork
        holv += i.holv; holk += i.holk
        pizv += i.pizv; pizk += i.pizk
        alkv += i.alkv; alkk += i.alkk
        desv += i.desv; desk += i.desk
        kofv += i.kofv; kofk += i.kofk
        allv += (i.gorv+i.holv+i.pizv+i.alkv+i.desv+i.kofv); allk += (i.gork+i.holk+i.pizk+i.alkk+i.desk+i.kofk)
        
    gorv = int (gorv); gork = int (gork); 
    holv = int (holv); holk = int (holk); 
    pizv = int (pizv); pizk = int (pizk); 
    desv = int (desv); desk = int (desk); 
    kofv = int (kofv); kofk = int (kofk); 
    alkv = int (alkv); alkk = int (alkk); 
    allv = int (allv); allk = int (allk)
    nm = 6 # количество строк в массиве

    # вычисляю проценты    

    # готовим массив
    mas.append( {
        'name': ('Горячее:' + GetDPercent (allv, gorv)),
        'v': gorv,
        'k': gork,
        'n': 0,
    } )

    mas.append( {
        'name': ('Холодное:' + GetDPercent (allv, holv)),
        'v': holv,
        'k': holk,
        'n': 1,
    } )

    mas.append( {
        'name': ('Пицца:' + GetDPercent (allv, pizv)),
        'v': pizv,
        'k': pizk,
        'n': 2,
    } )

    mas.append( {
        'name': ('Дессерт:' + GetDPercent (allv, desv)),
        'v': desv,
        'k': desk,
        'n': 3,
    } )

    mas.append( {
        'name': ('Кофе/Чай:' + GetDPercent (allv, kofv)),
        'v': kofv,
        'k': kofk,
        'n': 4,
    } )

    mas.append( {
        'name': ('Алкоголь:' + GetDPercent (allv, alkv)),
        'v': alkv,
        'k': alkk,
        'n': 5,
    } )

    st = {
        'allv': allv,
        'allk': allk,
        'nm': nm,
        'data': mas,
    }

    return st



def DenDiagramm (Request):

    # выводим диаграмму рабочих дней (Выручка по группам блюд, количество по группам блюд)
    omas = []
    objset = 0

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    r = Receiver.objects.all()

    st={'name': '[Все]', 'id': 0}
    omas.append(st)

    for w in r:
        st={'name': w.name, 'id': w.pk}
        omas.append(st)
    
    begindate = datetime.date.today()
    enddate = datetime.date.today()
    ddate1 = f'{begindate:%Y-%m-%d}'
    ddate2 = f'{enddate:%Y-%m-%d}'

    mas = GetDRoundData ('', ddate1, ddate2)

    dform = DenForm ()

    if Request.method == 'POST':
        dform = DenForm (Request.POST)
        
        if dform.is_valid(): 

            # заполняем данные из формы
            ddate1 = Request.POST['b_date']
            ddate2 = Request.POST['e_date']
            ob = Request.POST['ob_field']
            if ob != '0':
                objset = int (ob)
                #objset = Receiver.objects.get(pk=b)

            mas = GetDRoundData (ob, ddate1, ddate2)

    return render(Request, 'catalog/dendiagramm.html', {'bdate': ddate1, 'edate': ddate2, 'user': Request.user, 
        'menu': mn, 'title': 'Рабочие дни (Диаграмма)', 'form': dform, 'omas': omas, 'masdata': mas, 'objset': objset,
        })

#Возврат json по запросу из приложения Bot
def DenDiagrammRound (Request, oid, d1, d2):

    mas = [] # возвращаемый массив данных из запроса  

    names = []
    values = []

    objid = int (oid)

    begindate = datetime.datetime.strptime(d1, '%Y-%m-%d').date()
    enddate = datetime.datetime.strptime(d2, '%Y-%m-%d').date()

    if objid != 0:
        ob = Receiver.objects.get(pk=objid)
        rep = Den.objects.filter(date__range=[begindate, enddate], obj=ob).order_by('date')
    else:
        rep = Den.objects.filter(date__range=[begindate, enddate]).order_by('date')


    # Считаем данные
    gorv = 0; holv = 0; pizv = 0; alkv = 0; desv = 0; kofv = 0; all = 0

    for i in rep:
        gorv += i.gorv
        holv += i.holv
        pizv += i.pizv
        alkv += i.alkv
        desv += i.desv
        kofv += i.kofv
        all += all + (i.gorv+i.holv+i.pizv+i.alkv+i.desv+i.kofv)

    # готовим массив
    mas.append( {
        'name': 'Горячее',
        'v': gorv,
    } )

    names.append('Горячее')
    values.append(gorv)

    mas.append( {
        'name': 'Холодное',
        'v': holv,
    } )

    names.append('Холодное')
    values.append(holv)

    mas.append( {
        'name': 'Пицца',
        'v': pizv,
    } )

    names.append('Пицца')
    values.append(pizv)

    mas.append( {
        'name': 'Дессерт',
        'v': desv,
    } )

    names.append('Дессерт')
    values.append(desv)

    mas.append( {
        'name': 'Кофе/Чай',
        'v': kofv,
    } )

    names.append('Чай/Кофе')
    values.append(kofv)

    mas.append( {
        'name': 'Алкоголь',
        'v': alkv,
    } )

    names.append('Алкоголь')
    values.append(alkv)
    
    return JsonResponse({'masdata': mas, 'names': names, 'values': values, })   
