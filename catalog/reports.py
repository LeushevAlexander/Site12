from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from .models import Tabel, Vidnach, Podrazd, Receiver, Den, Graphic, Sotr
from .views import getmenu
from .forms import TabelReportSimpleForm, TabelReportForm, DenReportForm, GraphicDayReportSimpleForm, TabelReportSimpleFormPan

from datetime import datetime, date, timedelta

def TabelReportSimple(Request):
    #Отчет по табелю простой
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    # Всем пользователям доступен этот отчет
    # if Request.user.A_Tabel != True:
    #     # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
    #     return redirect('AccessDenied') 

    begindate = date.today()
    enddate = date.today()

    begindate = f'{begindate:%Y-%m-%d}'
    enddate = f'{enddate:%Y-%m-%d}'

    vnach = Vidnach.objects.get(pk=1) #отбираем только начисления по табелю
    divis= Podrazd.objects.all()
    obj=Receiver.objects.all()
    dmas = []
    all_kol = 0
    all_smn = 0

    # сначала делаем запрос с информацией о времени работы
    # в конце мы делаем такой же запрос но без времени, что ты в списке не было много одинаковой информации
    # и присоединяем ей информацию о времени ))

    if Request.user.A_TabelReport == True:
        # отбора по сотруднику нет, смотрим всех
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))
    else:
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

    if Request.method == 'POST':
        
        formreport = TabelReportSimpleForm(Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            if Request.user.A_TabelReport == True:
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))
            else:
                # отбор по сотруднику указанному в пользователе
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

            for i in rep:                
                print(i)

            # теперь надо сформировать таблицу для вывода по объектам и подразделениям
            dmas = []

            for d in divis:
                #пробегаюсь по rep, смотрю есть ли записи с объектом o
                f=0
                d_kl=0
                d_sm=0

                for r in rep:
                    if d.pk==int(r['div']):
                        f=1 # нашли запись
                        
                        if r['kol__sum'] is None:
                            kk = 0
                        else:
                            kk = float(r['kol__sum'])
                        d_kl+=kk
#                       d_kl+=float(r['kol__sum'])
                        d_sm+=int(r['id__count'])

                if f== 1: # Добавляем запись в массив подразделений
                    rec={
                        'divis': d,
                        'kol': round (d_kl, 2),
                        'sm': d_sm
                    }

                    dmas.append(rec)
                    all_kol+=round (d_kl, 2)
                    all_smn+=d_sm
    else:
        formreport = TabelReportSimpleForm()

    for t in rep:
        # добавляю поле со списком выписанных документов по сотруднику
        st=''
        ind=1

        for i in tb:
            k=0
            if (t['sotr__id']==i.sotr.id):
                #делаем строку и устанавливанм ее как docs
                st += str(ind)+')  ' + f'{i.date:%d-%m-%Y}' + ': ' + str(i.kol) + ' (' + str(i.t1) + ':' + str(i.t2) + ')<br>'
                ind+=1

                # Заодно округляю кол-во часов
                if t['kol__sum'] is None:
                    kk = 0
                else:
                    kk = round (t['kol__sum'], 2)

                # t['kol__sum'] = round (t['kol__sum'], 2)
                t['kol__sum'] = kk

        t['docs'] = st

    #Надо заново сформировать rep (без детализации по времени)
    if Request.user.A_TabelReport == True:
        # отбора по сотруднику нет, смотрим всех
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))
    else:
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))

    if Request.method == 'POST':
        
        formreport = TabelReportSimpleForm(Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            if Request.user.A_TabelReport == True:
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))
            else:
                # отбор по сотруднику указанному в пользователе
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))

    # пробегаюсь по таблице rep1 и переношу данные поля docs из таблицы rep
    for i in rep1:
        for t in rep:
            if i['sotr__id'] == t['sotr__id']:
                i['docs'] = t['docs']
                # Заодно округляю кол-во часов
                i['kol__sum'] = round (i['kol__sum'], 2)
                break

    return render(Request, 'catalog/tabelreportsimple.html', {'rep': rep1, 'form': formreport, 'divis': dmas, 'obj': obj, 'user': Request.user, 
        'menu': mn, 'title': 'Отчет по табелю, простой.', 
        'begindate': begindate, 'enddate': enddate, 'akol': all_kol, 'asm': all_smn,
        })

def TabelReport(Request):

    #Отчет по табелю 
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_TabelReportAdmin != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    begindate = date.today()
    enddate = date.today()

    begindate = f'{begindate:%Y-%m-%d}'
    enddate = f'{enddate:%Y-%m-%d}'

    vnach = Vidnach.objects.all()
    divis= Podrazd.objects.all()
    obj=Receiver.objects.all()

    dmas = []
    all_kol = 0
    all_smn = 0
    all_sum = 0
    vnch = 0
    ob = 0

    vmas = []

    st={'name': '[Все]', 'id': 0}
    vmas.append(st)

    for w in vnach:
        st={'name': w.name, 'id': w.pk}
        vmas.append(st)

    omas = []
    st={'name': '[Все]', 'id': 0}    
    omas.append(st)
    for w in obj:
        st={'name': w.name, 'id': w.pk}
        omas.append(st)

    # отбора по сотрудникам нету
    # сначала делаем запрос с информацией о времени работы
    # в конце мы делаем такой же запрос но без времени, что ты в списке не было много одинаковой информации
    # и присоединяем ей информацию о времени ))

    tb = Tabel.objects.filter(date__range=[begindate, enddate]).order_by('date') # для формирования отчета сотрудников по записям за период    
    rep = Tabel.objects.filter(date__range=[begindate, enddate]).values('sotr__name', 'sotr__id', 'div', 'stavka', 't1', 't2').annotate(Sum('kol'), Count('id'), Sum('sum'))

    if Request.method == 'POST':
        
        formreport = TabelReportForm(Request.POST)
        
        if formreport.is_valid(): 
    
            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            vnch = Request.POST['vnach_field']
            # divs = Request.POST['divis']
            # ob = Request.POST['obj']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            vnch=int(vnch)

            ob = Request.POST['ob_field']
            ob = int(ob)
            
            if vnch==0:
                if ob==0:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate]).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep = Tabel.objects.filter(date__range=[begindate, enddate]).values('sotr__name', 'sotr__id', 'div', 'stavka', 't1', 't2').annotate(Sum('kol'), Count('id'), Sum('sum'))
                else: # фильтруем по объекту
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], obj=ob).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep = Tabel.objects.filter(date__range=[begindate, enddate], obj=ob).values('sotr__name', 'sotr__id', 'div', 'stavka', 't1', 't2').annotate(Sum('kol'), Count('id'), Sum('sum'))
            else:
                # делаем отбор по виду начисления (табель, премия и т.д.)
                if ob==0:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch).values('sotr__name', 'sotr__id', 'div', 'stavka', 't1', 't2').annotate(Sum('kol'), Count('id'), Sum('sum'))
                else: # фильтуем по объекту
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch, obj=ob).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch, obj=ob).values('sotr__name', 'sotr__id', 'div', 'stavka', 't1', 't2').annotate(Sum('kol'), Count('id'), Sum('sum'))

            # for i in rep:                
            #     print(i)
            # Не выводим, не надо ))

            # теперь надо сформировать таблицу для вывода по объектам и подразделениям
            dmas = []

            for d in divis:
                #пробегаюсь по rep, смотрю есть ли записи с объектом o
                f=0
                d_kl=0
                d_sm=0
                d_sum=0

                for r in rep:
                    if d.pk==int(r['div']):
                        f=1 # нашли запись
                        
                        kk = r['kol__sum']
                        if kk is None:
                            kk = 0
                        
                        #d_kl+=round(float(r['kol__sum']), 2)
                        d_kl+=round(kk, 2)

                        d_sm+=int(r['id__count'])

                        kk = r['sum__sum']
                        if kk is None:
                            kk = 0

                        #d_sum+=round(float(r['sum__sum']), 2)
                        d_sum+=round(kk, 2)

                if f== 1: # Добавляем запись в массив подразделений
                    rec={
                        'divis': d,
                        'kol': round(d_kl, 2),
                        'sm': round(d_sm, 2),
                        'sum': round(d_sum, 2),
                    }

                    dmas.append(rec)
                    all_kol+=d_kl
                    all_smn+=d_sm
                    all_sum+=d_sum
    else:
        formreport = TabelReportForm()

    for t in rep:
        # добавляю поле со списком выписанных документов по сотруднику
        st=''
        ind=1

        for i in tb:
            k=0
            if (t['sotr__id']==i.sotr.id):
                #делаем строку и устанавливанм ее как docs
                st += str(ind)+')  ' + f'{i.date:%d-%m-%Y}' + ': ' + str(i.sum) + ' (' + str(i.kol) + ') (' + str(i.t1) + '-' + str(i.t2) + ')<br>'
                ind+=1

        t['docs'] = st

    #Надо заново сформировать rep (без детализации по времени)
    rep1 = Tabel.objects.filter(date__range=[begindate, enddate]).values('sotr__name', 'sotr__id', 'div', 'stavka').annotate(Sum('kol'), Count('id'), Sum('sum'))

    if Request.method == 'POST':
        
        formreport = TabelReportForm(Request.POST)
        
        if formreport.is_valid(): 
            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            vnch = Request.POST['vnach_field']
            # divs = Request.POST['divis']
            ob = Request.POST['ob_field']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            vnch=int(vnch)
            ob=int(ob)
            
            if vnch==0:
                if ob==0:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate]).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep1 = Tabel.objects.filter(date__range=[begindate, enddate]).values('sotr__name', 'sotr__id', 'div', 'stavka').annotate(Sum('kol'), Count('id'), Sum('sum'))
                else:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], obj=ob).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep1 = Tabel.objects.filter(date__range=[begindate, enddate], obj=ob).values('sotr__name', 'sotr__id', 'div', 'stavka').annotate(Sum('kol'), Count('id'), Sum('sum'))                    
            else:
                # делаем отбор по виду начисления (табель, премия и т.д.)
                if ob==0:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch).values('sotr__name', 'sotr__id', 'div', 'stavka').annotate(Sum('kol'), Count('id'), Sum('sum'))
                else:
                    tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch, obj=ob).order_by('date') # для формирования отчета сотрудников по записям за период    
                    rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnch, obj=ob).values('sotr__name', 'sotr__id', 'div', 'stavka').annotate(Sum('kol'), Count('id'), Sum('sum'))                    

    # пробегаюсь по таблице rep1 и переношу данные поля docs из таблицы rep
    for i in rep1:
        for t in rep:
            if i['sotr__id'] == t['sotr__id']:
                i['docs'] = t['docs']
                # заодно округляем сумму денег ))
                i['kol__sum'] = round (i['kol__sum'], 2)
                i['sum__sum'] = round (i['sum__sum'], 2)
                break

    return render(Request, 'catalog/tabelreport.html', {'rep': rep1, 'form': formreport, 
        'vnach': vmas, 'divis': dmas, 'obj': omas, 'user': Request.user, 
        'menu': mn, 'title': 'Отчет по табелю.', 
        'begindate': begindate, 'enddate': enddate, 'akol': round(all_kol), 'asm': round(all_smn, 2), 'asum': round(all_sum, 2), 
        'vnch': vnch, 'ob': ob,
        })

def TabelReportSimplePan(Request):


    #Отчет по табелю простой
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    # Всем пользователям доступен этот отчет
    # if Request.user.A_Tabel != True:
    #     # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
    #     return redirect('AccessDenied') 

    begindate = date.today()
    enddate = date.today()

    begindate = f'{begindate:%Y-%m-%d}'
    enddate = f'{enddate:%Y-%m-%d}'

    vnach = Vidnach.objects.get(pk=1) #отбираем только начисления по табелю
    divis= Podrazd.objects.all()
    obj=Receiver.objects.all()
    dmas = []
    all_kol = 0
    all_smn = 0

    # сначала делаем запрос с информацией о времени работы
    # в конце мы делаем такой же запрос но без времени, что ты в списке не было много одинаковой информации
    # и присоединяем ей информацию о времени ))

    if Request.user.A_TabelReport == True:
        # отбора по сотруднику нет, смотрим всех
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))
    else:
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

    if Request.method == 'POST':
        
        formreport = TabelReportSimpleForm(Request.POST)
        
        if formreport.is_valid(): 

            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            if Request.user.A_TabelReport == True:
                objrep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('obj').annotate(Sum('kol'), Count('id')) # для формирования по объектам
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('date', 'sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))
            else:
                # отбор по сотруднику указанному в пользователе
                objrep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('obj').annotate(Sum('kol'), Count('id'))
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div', 't1', 't2').annotate(Sum('kol'), Count('id'))

            #for i in rep:                
            #    print(i)

            # выводим по объектам


            # теперь надо сформировать таблицу для вывода по объектам и подразделениям
            dmas = []

            for d in divis:
                #пробегаюсь по rep, смотрю есть ли записи с объектом o
                f=0
                d_kl=0
                d_sm=0

                for r in rep:
                    if d.pk==int(r['div']):
                        f=1 # нашли запись
                        
                        if r['kol__sum'] is None:
                            kk = 0
                        else:
                            kk = float(r['kol__sum'])
                        d_kl+=kk
#                       d_kl+=float(r['kol__sum'])
                        d_sm+=int(r['id__count'])

                if f== 1: # Добавляем запись в массив подразделений
                    rec={
                        'divis': d,
                        'kol': round (d_kl, 2),
                        'sm': d_sm
                    }

                    dmas.append(rec)
                    all_kol+=round (d_kl, 2)
                    all_smn+=d_sm
    else:
        formreport = TabelReportSimpleFormPan()

    for t in rep:
        # добавляю поле со списком выписанных документов по сотруднику
        st=''
        ind=1

        for i in tb:
            k=0
            if (t['sotr__id']==i.sotr.id):
                #делаем строку и устанавливанм ее как docs
                st += str(ind)+')  ' + f'{i.date:%d-%m-%Y}' + ': ' + str(i.kol) + ' (' + str(i.t1) + ':' + str(i.t2) + ')<br>'
                ind+=1

                # Заодно округляю кол-во часов
                if t['kol__sum'] is None:
                    kk = 0
                else:
                    kk = round (t['kol__sum'], 2)

                # t['kol__sum'] = round (t['kol__sum'], 2)
                t['kol__sum'] = kk

        t['docs'] = st

    #Надо заново сформировать rep (без детализации по времени)
    if Request.user.A_TabelReport == True:
        # отбора по сотруднику нет, смотрим всех
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))
    else:
        tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
        rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))

    if Request.method == 'POST':
        
        formreport = TabelReportSimpleForm(Request.POST)
        
        if formreport.is_valid(): 


            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            #tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
            if Request.user.A_TabelReport == True:
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))
            else:
                # отбор по сотруднику указанному в пользователе
                tb = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).order_by('date') # для формирования отчета сотрудников по записям за период    
                rep1 = Tabel.objects.filter(date__range=[begindate, enddate], vidnach=vnach, sotr=Request.user.sotr).values('sotr__name', 'sotr__id', 'obj', 'div').annotate(Sum('kol'), Count('id'))

    # пробегаюсь по таблице rep1 и переношу данные поля docs из таблицы rep
    for i in rep1:
        for t in rep:
            if i['sotr__id'] == t['sotr__id']:
                i['docs'] = t['docs']
                # Заодно округляю кол-во часов
                i['kol__sum'] = round (i['kol__sum'], 2)
                break

    return render(Request, 'catalog/tabelreportsimplepan.html', {'rep': rep1, 'form': formreport, 'divis': dmas, 'obj': obj, 'user': Request.user, 
        'menu': mn, 'title': 'Отчет по табелю, простой.', 
        'begindate': begindate, 'enddate': enddate, 'akol': all_kol, 'asm': all_smn,
        })



def DN (Num):
    s = '{0:,}'.format(Num).replace(',', ' ')
    return s

def DenReport(Request):
    
    #Отчеты за день 
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_DenReport != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    begindate = date.today()
    enddate = date.today()

    begindate = f'{begindate:%Y-%m-%d}'
    enddate = f'{enddate:%Y-%m-%d}'

    rlist = Receiver.objects.all()
    mas = []
    ast = {}
    itflag = 0 # по умолчанию не выводим итог

    rep = Den.objects.filter(date__range=[begindate, enddate]).values('date', 'obj', 'pk').annotate(Sum('vnal'), Sum('vbnal'), Sum('kolg'), Sum('kolblud'), Sum('masblud'), Sum('chn'), Sum('chbn')).order_by('date', 'obj')
    for i in rep: print (i)

    if Request.method == 'POST':
        
        formreport = DenReportForm(Request.POST)
        
        if formreport.is_valid(): 
    
            # из формы получаю начальную дату и конечную, перезаполняю отчет
            # все вычисления делаю в html

            begindate = Request.POST['b_date']
            enddate = Request.POST['e_date']

            rep = Den.objects.filter(date__range=[begindate, enddate]).values('date', 'obj', 'pk').annotate(Sum('vnal'), Sum('vbnal'), Sum('kolg'), Sum('kolblud'), Sum('masblud'), Sum('chn'), Sum('chbn')).order_by('date', 'obj')
            for i in rep: print (i)

            # создаю таблицу вывода рабочих дней 
            day=timedelta(days=1)
            
            d=datetime.strptime(begindate, '%Y-%m-%d')
            ed=datetime.strptime(enddate, '%Y-%m-%d')

            # Суммируем количество показателей для передачи в таблицу
            av_e = 0; av_m = 0; av_em = 0; # Вся выручка за период
            ak_e = 0; ak_m = 0; ak_em = 0; # Все кол часов за период
            ag_e = 0; ag_m = 0; ag_em = 0; # Все кол во гостей
            ac_e = 0; ac_m = 0; ac_em = 0; # Весь чай

            while d <= ed:
                
                # создаю запись по рабочим дням за дату
                v_e=0; v_m=0; kg_e=0; kg_m=0; kc_e=0; kc_m=0; kb_e=0; kb_m=0; mb_e=0; mb_m=0; ch_e=0; ch_m=0; ch_em=0
                cc_e=0; cc_m=0; cc_em=0

                for r in rep:
                    if r['date'] == d.date():
                        #нашли дату пробегаемся по массиву объектов и увеличиваю количество показателей
                        for j in rlist:
                            if (j.pk == 1 and r['obj'] == j.pk): # Марта
                                v_m+=(r['vnal__sum']+r['vbnal__sum'])
                                kg_m+=r['kolg__sum']
                                kb_m+=r['kolblud__sum']
                                mb_m+=r['masblud__sum']
                                ch_m+=(r['chn__sum']+r['chbn__sum'])
                                kb_m=ch_m

                            elif (j.pk == 2 and r['obj'] == j.pk): # EL GUSTO
                                v_e+=(r['vnal__sum']+r['vbnal__sum'])
                                kg_e+=r['kolg__sum']
                                kb_e+=r['kolblud__sum']
                                mb_e+=r['masblud__sum']
                                ch_e+=(r['chn__sum']+r['chbn__sum'])
                                kb_e=ch_e
                
                # определяю количество часов по каждому заведению
                tb1 = Tabel.objects.filter(date=d.date(), obj=1).values('date',
                    'obj').annotate(Sum('kol')) # Это Марта
                for w in tb1: print (w)
                if len(tb1) > 0:
                    kc_m=tb1[0]['kol__sum']

                tb2 = Tabel.objects.filter(date=d.date(), obj=2).values('date',
                    'obj').annotate(Sum('kol')) # Это EL GUSTO
                for w in tb2: print (w)
                if len(tb2) > 0:
                    kc_e=tb2[0]['kol__sum']

                # определяю цвет фона в зависимости от кол-ва часов
                ck_e = 0; ck_m = 0; ck_em = 0
                
                kc_e = round (kc_e, 1)
                kc_m = round (kc_m)

                if kc_e != 0:
                    k = float (v_e / kc_e)
                    if k < 800:
                        k = 0  # Красный
                    elif (k >= 800 and k < 1000):
                        k = 1 # Желтый
                    else:
                        k = 2 # Зеленый
                else:
                    k = 0 # Красный, не заполнено

                ck_e = k # Цвет поля в эльгусто

                if kc_m != 0:
                    k = float (v_m / kc_m)
                    if k < 800:
                        k = 0  # Красный
                    if (k >= 800 and k < 1000):
                        k = 1 # Желтый
                    if k >= 1000:
                        k = 2 # Зеленый
                else:
                    k = 0 # Красный, не заполнено

                ck_m = k # Цвет поля в Марта

                if (kc_e + kc_m) != 0:
                    k = float ((v_e + v_m) / (kc_e + kc_m))
                    if k < 800:
                        k = 0  # Красный
                    if (k >= 800 and k < 1000):
                        k = 1 # Желтый
                    if k >= 1000:
                        k = 2 # Зеленый
                else:
                    k = 0 # Красный, не заполнено

                ck_em = k # Цвет поля общий

                if (v_e+v_m) != 0:
                    ch_em = float ((ch_m+ch_e) / (v_m+v_e) * 100)
                else:
                    ch_em = 3 # норма

                if v_e != 0:
                    ch_e = float (ch_e / v_e * 100)
                else:
                    ch_e = 3 # норма

                if v_m != 0:
                    ch_m = float (ch_m / v_m * 100)
                else:
                    ch_m = 3 # норма
                
                if ch_e <= 1:
                    cc_e=0 # черный
                if ch_e > 1 and ch_e <= 2:
                    cc_e=1 # красный
                if ch_e > 2 and ch_e <=4:
                    cc_e=2 # желтый
                if ch_e > 4:
                    cc_e=3 # зеленый

                if ch_m <= 1:
                    cc_m=0 # черный
                if ch_m > 1 and ch_m <= 2:
                    cc_m=1 # красный
                if ch_m > 2 and ch_m <=4:
                    cc_m=2 # желтый
                if ch_m > 4:
                    cc_m=3 # зеленый

                if ch_em <= 1:
                    cc_em=0 # черный
                if ch_em > 1 and ch_em <= 2:
                    cc_em=1 # красный
                if ch_em > 2 and ch_em <=4:
                    cc_em=2 # желтый
                if ch_em > 4:
                    cc_em=3 # зеленый

                # кол-во блюд не использум, вместо него используем сумму чая
                # kb_e = ch_e; kb_m = ch_m; 

                rflag = 0 # по умолчанию вывод строки 'не выводим'

                if (v_e + v_m + kc_e + kc_m + kb_e + kb_m + kg_e + kg_m) > 0:
                    rflag = 1

                # вставляю запись по рабочему дню общую, в таблицу уже
                st={'date': d.date(), 
                    'v_e': DN (v_e), 'v_m': DN (v_m), 'v_em': DN ((v_e + v_m)), # выручка (elgusto, marta, elgusto+marta)
                    'kc_e': DN (kc_e), 'kc_m': DN (kc_m), 'kc_em': DN ((kc_e + kc_m)), # кол час (elgusto, marta, elgusto+marta)
                    'kb_e': DN (kb_e), 'kb_m': DN (kb_m), 'kb_em': DN ((kb_e + kb_m)), # ---кол блюд--- сумма чая (elgusto, marta, elgusto+marta)
                    'mb_e': mb_e, 'mb_m': mb_m, 'mb_em': round((mb_e + mb_m), 1), # масса блюд (elgusto, marta, elgusto+marta)
                    'kg_e': DN (kg_e), 'kg_m': DN (kg_m), 'kg_em': DN ((kg_e + kg_m)),    # кол гостей (elgusto, marta, elgusto+marta)
                    'ck_e': ck_e, 'ck_m': ck_m, 'ck_em': ck_em, # цвет фона от количества часов (elgusto, marta, elgusto+marta)
                    'ch_e': round(ch_e, 1), 'ch_m': round(ch_m, 1), 'ch_em': round(ch_em, 1), # цвет фона от суммы чая (elgusto, marta, elgusto+marta)
                    'cc_e': cc_e, 'cc_m': cc_m, 'cc_em': cc_em,
                    'rflag': rflag,
                }
                mas.append(st)
                d+=day

                # Суммируем показатели для передачи
                av_e = av_e + v_e; av_m = av_m + v_m; av_em = av_em + (v_e + v_m); 
                ak_e = ak_e + kc_e; ak_m = ak_m + kc_m; ak_em = ak_em + (kc_e + kc_m); 
                ag_e = ag_e + kg_e; ag_m = ag_m + kg_m; ag_em = ag_em + (kg_e + kg_m); 
                ac_e = ac_e + kb_e; ac_m = ac_m + kb_m; ac_em = ac_em + (kb_e + kb_m);  # Чай
                
                ak_e = round (ak_e, 1); ak_m = round (ak_m, 1); ak_em = round (ak_em)
                acp_e = 0; acp_m = 0; acp_em = 0; # процент чая

                # определяю процент чая
                if av_e != 0:
                    acp_e = float (ac_e / av_e * 100)
                    acp_e = round (acp_e, 1)                    
                
                if av_m != 0:
                    acp_m = float (ac_m / av_m * 100)
                    acp_m = round (acp_m, 1)
                
                if av_em != 0:
                    acp_em = float (ac_em / av_em * 100)
                    acp_em = round (acp_em)
    
            if (av_em + ak_em + ag_em + ac_em + acp_em) > 0:
                itflag = 1

            ast = {
                'av_e': DN (av_e), 'av_m': DN (av_m), 'av_em': DN (av_em),
                'ak_e': DN (ak_e), 'ak_m': DN (ak_m), 'ak_em': DN (ak_em),
                'ag_e': DN (ag_e), 'ag_m': DN (ag_m), 'ag_em': DN (ag_em),
                'ac_e': DN (ac_e), 'ac_m': DN (ac_m), 'ac_em': DN (ac_em),
                'acp_e': (DN (acp_e) + '%'), 'acp_m': (DN (acp_m) + '%'), 'acp_em': (DN (acp_em) + '%'),
            }                
    
    else:
        formreport = DenReportForm()

    return render(Request, 'catalog/denreport.html', {'rep': mas, 'form': formreport, 'ast': ast, 'itflag': itflag,
        'user': Request.user, 'menu': mn, 'title': 'Отчет по дням.', 
        'begindate': begindate, 'enddate': enddate,  
        })
