from django.shortcuts import redirect, render
from json import loads
from .views import getmenu
from django.db.models import Q
from .forms import STaskForm
from .models import Receiver, Source, Sotr, STask, STaskPriority, STaskType
import datetime

def STaskRecDel (Request, bpk):

    # удаляем запись из рабочих дней, физически
    b = int (bpk)

    STask.objects.filter(pk=b).delete ()
    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def GetF (st):

    val = 0

    if st == '':
        st = '0.0'

    st = st.replace(',', '.')
    val = float(st)

    return val

def STaskRecEdit (Request):

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

def STaskRecAdd (Request):

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

def STaskView (Request):
    
    
    # выводим задачи
    tmas = [] # список задач
    omas = [] # список объектов
    dmas = [] # список подразделений
    tpmas = [] # список типов
    pmas = [] # список приоритетов
    smas = [] # список сотрудников

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    omas = Receiver.objects.all()
    dmas = Source.objects.all()
    tpmas = STaskType.objects.all()
    pmas = STaskPriority.objects.all()
    smas = Sotr.objects.filter(active=True)

    begindate = datetime.date.today()
    enddate = datetime.date.today()

    ddate1 = f'{begindate:%Y-%m-%d}'
    ddate2 = f'{enddate:%Y-%m-%d}'

    tdate = ddate1

    begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')

    t = STask.objects.filter(date__range=[ddate1, ddate2], active=True).order_by('date')

    if Request.method == 'POST':
        tform = STaskForm (Request.POST)
        
        if tform.is_valid(): 

            # заполняем данные из формы
            ddate1 = Request.POST['d_date1']
            ddate2 = Request.POST['d_date2']

            t = STask.objects.filter(date__range=[ddate1, ddate2], active=True).order_by('date')

        else:
            tform = STaskForm ()
        
    return render(Request, 'catalog/staskview.html', {'bdate': ddate1, 'edate': ddate2, 'tdate': tdate, 'user': Request.user, 
        'menu': mn, 'title': 'Задачи сотрудников', 'form': tform, 'dmas': dmas, 'omas': omas, 'tmas': t, 'tpmas': tpmas, 
        'pmas': pmas, 'smas': smas,
        })


