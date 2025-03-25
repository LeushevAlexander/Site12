from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now

from .views import getmenu
from .models import NomenHim, Ei, Source, Receiver, ZakazHim, ZakazremarkHim

import datetime
from json import loads

# Create your views here.
from .forms import AddZakazHimForm, ExeZakazHimForm, AddZakazremarkHimForm, NomenHimForm
from django.db.models import Q

def AddZakazHim(Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    sstr = '' # строка поиска

    nomenlist = NomenHim.objects.order_by('name')  # Список номенклатуры
    elist = Ei.objects.all() # Список единиц измерения
    slist = Source.objects.all() # Список источников (баз)
    rlist = Receiver.objects.all() # Список мест объектов производства / по умолчанию - тот, который в пользователе

    dt = datetime.date.today()
    zakazdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':

        formzakaz = AddZakazHimForm(Request.POST)
        if formzakaz.is_valid(): 
            
            # нажали кнопку создания заявки, необходимо ее обработать ))
            # и создать запись в заявке )))
            mas = []

            zd = Request.POST['zakaz_date']
            zdate = datetime.datetime.strptime(zd, '%Y-%m-%d')
            zakazdate = zd
            #source = Request.POST['zakaz_source']
            receiver = Request.POST['zakaz_receiver']
            searchstring = Request.POST['searchstring']

            # определяю, нажата ли клавиша поиск...
            ch = Request.POST['choise']

            if ch=='search':

                # нажата клавиша поиск, выполняем команду поиска, обновляем, ничего не создаем
                
                if searchstring != '':
                    # надо отфильтровать по строке
                    searchstring=searchstring.upper()
                    nomenlist = NomenHim.objects.filter(name__icontains=searchstring).order_by('name')  # Список номенклатуры фильтрую по строке
                    nlist = NomenHim.objects.filter(name__icontains=searchstring).order_by('name')
                    sstr = searchstring
                else:
                    nlist = NomenHim.objects.all().order_by('name')
                    nomenlist = NomenHim.objects.all().order_by('name')

            if ch=='create':
                
                # надо создать, в зависимости от фильтра searchstring
                if searchstring != '':
                    # надо отфильтровать по строке
                    searchstring=searchstring.upper()
                    nomenlist = NomenHim.objects.filter(name__icontains=searchstring).order_by('name')  # Список номенклатуры фильтрую по строке
                    nlist = NomenHim.objects.filter(name__icontains=searchstring).order_by('name')
                    sstr = searchstring
                else:
                    nlist = NomenHim.objects.all().order_by('name')
                    nomenlist = NomenHim.objects.all().order_by('name')

                # надо найти как то  количество, которое я поставил ))
                for n in nlist:
                    st ='nomen' + str(n.id)
                    kol = Request.POST[st]
                    kol = kol.replace(',', '.')

                    if len(kol) > 0:
                                                            
                        kol = float(kol)
                        if kol != 0:
                        
                            sed='ei' + str(n.id)
                            ed= Request.POST[sed]    
                            ed=Ei.objects.get(id=ed)
                        
                            #вставляю в массив для заявки
                            rec = {
                                'nomen': n,
                                'kol': kol,
                                'edin': ed
                            }                        
                            mas.append(rec)

                        
                # пора формировать запись в базе
                for i in mas:
                    # добавяю запись в таблицу заявок
                    nm=i['nomen']
                    kl=i['kol']
                    #e=i['nomen'].ei
                    e=i['edin']
                    tm=now()
                    #sr=Source.objects.get(id=source)
                    sr=nm.source_link
                    rc=Receiver.objects.get(id=receiver)
                    cs=nm.cost
                                
                    z =ZakazHim (date=zdate, source_link=sr, receiver_link=rc, nomen_link=nm, creator=Request.user.username, 
                            cost=cs, kol=kl, ei_link=e, status=0, time_create=tm)                
                    z.save()
            
                #теперь надо перенаправить на страницу сообщения о создании заявки по следующим позициям
                if len(mas) > 0:
                    return render(Request, 'catalog/zakazhimcreated.html', {'nlist': mas, 'loginuser': usr, 
                    'menu': mn, 'title': 'Заявка на химию создана.', 'date_zakaz': zdate,   
                    'elist': elist, 'slist': slist, 'rlist': rlist, })
                    
    else:    
        formzakaz = AddZakazHimForm()        

    return render(Request, 'catalog/addzakazhim.html', {'nlist': nomenlist, 'form': formzakaz, 
        'loginuser': usr, 'menu': mn, 'title': 'Создание заказа на химию.', 
        'elist': elist, 'slist': slist, 'rlist': rlist, 'date_zakaz': zakazdate, 'zstr': sstr,
        })

def AddZakazremarkHim (Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    usr = Request.user

    #dt = datetime.date.today()
    dt = datetime.datetime.now()
    tdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':
        
        formremark = AddZakazremarkHimForm(Request.POST)
        if formremark.is_valid(): 
           
            # нажали кнопку создания заявки, необходимо ее обработать ))
            textremark = Request.POST['textremark']                                
            r =ZakazremarkHim (date=dt, creator=usr.username, remark=textremark, status=False, time_create=dt)
            r.save()
            
            #теперь надо перенаправить на страницу сообщения о создании табеля по следующим позициям
            tdate=f'{dt:%d-%m-%Y}'
            return render(Request, 'catalog/zakazremarkhimcreated.html', {'menu': mn, 'title': 'Комментарий сохранен.', 
                        'date_remark': tdate, 'textremark': textremark, 'creator': usr.username, })
           
    else:
        formremark = AddZakazremarkHimForm()

    return render(Request, 'catalog/addzakazremarkhim.html', {'remark': '', 'form': formremark, 
        'menu': mn, 'title': 'Создание комментария.', })


def ExeZakazHim(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    rm = []

    # заполняю комментарии к заявкам, выделенным цветом
    rmlist = ZakazremarkHim.objects.filter(status=False)

    # Вывожу список продуктов которые в заявке
    # где status < 2 и date <= дате на экране
    
    zlist = ZakazHim.objects.filter(Q(status=0)|Q(status=1)).order_by('nomen_link__name')

    sr = Source.objects.all() # список мест закупа
    td1 = datetime.timedelta(days=1)

    dc = []
    mz = []

    # теперь мне надо разделить номенклатуру по местам закупа (лента, магазин, рынок)
    for s in sr:
        ms = []

        # пробегаюсь по списку номенклатуры в заявке и группирую его по местам закупа
        for z in zlist:
            if z.source_link==s:
                # формирую строку записи и вставляю запись в список по данномму месту закупа
                # kol_m это количество Марта, kol_e это количество Эльгусто

                km=0
                ke=0

                if z.receiver_link.id == 1: # Колво в Марту
                    km=z.kol
                else: 
                    if z.receiver_link.id == 2: # Колво в Эльгусто
                        ke=z.kol
                kol=km+ke

                dstatus=0
                
                if z.date < (datetime.datetime.now().date()-td1):
                    dstatus=1 # Надо вывести красным

                stb = str (z.nomen_link.id) + ";" + str (s.id) + ";" + str (z.status) # Заказ, Source, Заказ_статус
                st={'nomen': z.nomen_link.name, 'nomen_id': z.nomen_link.id, 'kol_m': km, 'kol_e': ke, 'status': z.status, 'kol': kol, 
                    'odin': z.ei_link.name, 'dstatus': dstatus, 'btn': stb, 'cost': str(z.nomen_link.cost), 
                    'opisanie': z.nomen_link.opisanie, 'img': z.nomen_link.img, 'docs':dc  }

                # надо посмотреть, есть ли в списке уже такая номенклатура
                # и если есть, просто увеличить количество

                fl = 0

                for m in ms:
                    
                    if m.get('nomen_id') == z.nomen_link.id:
                        # надо увеличивать кол-во и валить
                        k1=m.get('kol_m')+km
                        k2=m.get('kol_e')+ke
                        k3=k1+k2

                        m.update({'kol_m': k1, 'kol_e': k2, 'kol': k3})
                        fl=1 # флаг о том, что добавлять не надо

                if fl == 0:
                    ms.append(st)  
        
        for m in ms:
            dc = []  
            docs = '<div style="font-size: 12px;">' # возвращаемая строка с документами

            #делаю список заявок для каждой номенклатуры
            for y in zlist:
                if m['nomen_id'] == y.nomen_link.pk:
                    # совпадает с номенклатурой, вставляю в dc
                    #st1 = {"date": f'{y.date:%Y-%m-%d}', "creator": y.creator, "kol": str(y.kol)}
                    st1 = f'{y.date:%Y-%m-%d}' + "  " + y.receiver_link.name +  "  Кол: " + str(y.kol) + " " + y.ei_link.name + "  " + y.creator + "<br>"
                    dc.append(st1)
                    docs += st1 
            docs += '</div>'

            # освежаем ms
            m.update({'docs': docs})
        
        if len(ms) > 0: 
            # делаю запись по месту закупа
            st = {'name': s.name, 'nomen': ms }
            mz.append(st)


    if Request.method == 'POST':

        exezakaz = ExeZakazHimForm(Request.POST)

        if exezakaz.is_valid(): 
            # обрабатываю нажатие кнопки
            choice_str = Request.POST['choise']

            # проверяем ремарка это или нет
            q=choice_str[:2]
            if q=='rm': # это ремарка, надо ее погасить и не трогать номенклатуру
                rpk = choice_str[2:]
                rpk = int(rpk)

                ZakazremarkHim.objects.filter(pk=rpk, status=False).update(status=True, maker=Request.user.username, time_make=datetime.datetime.now())
                return redirect('ExeZakazHim')
            
            # Иначе
            # Бомбим нажатие по кнопке номенклатуры
            id_list=choice_str.split(sep=';')
            nomen_id=int(id_list[0])
            source_id=int(id_list[1])
            sts=int(id_list[2])

            nomen_obj = NomenHim.objects.get(id=nomen_id)
            source_obj=Source.objects.get(id=source_id)

            # теперь надо сделать update в зависимости от статуса заказа
            if sts==0:
                #устанавливаем флаг 1 (значит заказ взят, но не доставлен)
                ZakazHim.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=0).update(status=1, maker=Request.user.username, time_make=datetime.datetime.now())
                return redirect('ExeZakazHim')
            
            elif sts==1:
                #устанавливаем флаг 2 (значит заказ и взят и доставлен)
                ZakazHim.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=1).update(status=2, deliver=Request.user.username, time_deliv=datetime.datetime.now())
                return redirect('ExeZakazHim')

    exezakaz = ExeZakazHimForm()                
    return render(Request, 'catalog/exezakazhim.html', {'nlist': mz, 'form': exezakaz, 'loginuser': usr, 
                        'menu': mn, 'title': 'Заявка на химию.', 'remark': rmlist, })

def SelExeZakazHim (Request, param_zakaz):

    # Бомбим нажатие по кнопке номенклатуры
    id_list=param_zakaz.split(sep=';')
    nomen_id=int(id_list[0])
    source_id=int(id_list[1])
    sts=int(id_list[2])

    nomen_obj = NomenHim.objects.get(id=nomen_id)
    source_obj=Source.objects.get(id=source_id)

    # теперь надо сделать update в зависимости от статуса заказа
    if sts==0:
        #устанавливаем флаг 1 (значит заказ взят, но не доставлен)
        ZakazHim.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=0).update(status=1, maker=Request.user.username, time_make=datetime.datetime.now())
            
    elif sts==1:
        #устанавливаем флаг 2 (значит заказ и взят и доставлен)
        ZakazHim.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=1).update(status=2, deliver=Request.user.username, time_deliv=datetime.datetime.now())

    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})

def NomenHimView (Request):
    
    # выводим список номенклатуры по химии
    nmas = [] # список номенклатуры
    emas = [] # список единиц измерения
    smas = [] # список мест закупа

    filterstr = ''

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    nmas = NomenHim.objects.all().order_by('name') # список номенклатуры
    emas = Ei.objects.all() # список единиц измерения
    smas = Source.objects.all() # список мест закупа

    if Request.method == 'POST':
        nform = NomenHimForm (Request.POST)
        
        if nform.is_valid(): 
            # заполняем данные из формы (фильтр)
            filterstr = Request.POST['filter_name']
            nmas = NomenHim.objects.filter(name__icontains=filterstr).order_by('name')  # Список фильтрую по строке
        else:
            nform = NomenHimForm ()
    else:        
        nform =NomenHimForm ()
        
    return render(Request, 'catalog/nomenhimview.html', {'user': Request.user, 
        'menu': mn, 'title': 'Номенклатура (химия)', 'form': nform, 'nmas': nmas, 'emas': emas, 'smas': smas, 'filterstr': filterstr,
    })

def NomenHimRecAdd (Request):

    # считываем запись из окна создания
    eiset = Ei.objects.get(pk=int(loads(Request.body)['ei']))
    sourceset = Source.objects.get(pk=int(loads(Request.body)['source']))
    st = loads(Request.body)['cost'] 
    if st =='':
        st = '0'

    cost = int(st)

    name = (loads(Request.body)['name'])

    # теперь сохраняем данные в базе
    r = NomenHim(name=name, 
                 cost=cost,
                 ei=eiset,
                 source_link=sourceset,
                )    
    r.save()

    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def NomenHimRecEdit (Request):

    # считываем запись из номенклатуры 
    pk = int (loads(Request.body)['pk'])
    eiset = Ei.objects.get(pk=int(loads(Request.body)['ei']))
    sourceset = Source.objects.get(pk=int(loads(Request.body)['source']))
    st = loads(Request.body)['cost'] 
    if st =='':
        st = '0'

    cost = int(st)
    name = (loads(Request.body)['name'])

    # теперь изменяем данные в базе
    NomenHim.objects.filter(pk=pk).update(name=name, 
                 cost=cost,
                 ei=eiset,
                 source_link=sourceset
                )    

    return render (Request, 'catalog/accessdenied.html', {'title': ''})
