from django.shortcuts import redirect, render
from json import loads
from .views import getmenu
from django.db.models import Q
from .forms import BanketForm
from .models import Receiver, Banket, Vidopl, Vidmer
import datetime

def BanketRecDel (Request, bpk):

    # удаляем запись из банкетов (active ставим false)
    b = int (bpk)

    Banket.objects.filter(pk=b).update(active=False)    
    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def BanketRecEdit (Request):

    # считываем запись из банкетов 
    pk = int (loads(Request.body)['pk'])
    dt = datetime.datetime.strptime((loads(Request.body)['dt']), '%Y-%m-%d').date()
    vmerset = Vidmer.objects.get(pk=int(loads(Request.body)['vmer']))
    objset = Receiver.objects.get(pk=int(loads(Request.body)['obj']))
    
    st = loads(Request.body)['sum'] 
    if st =='':
        st = '0'

    sum = int(st)

    voplset = Vidopl.objects.get(pk=int(loads(Request.body)['vopl']))

    st = loads(Request.body)['kolg']
    if st =='':
        st = '0'

    kolg = int (st)

    st = loads(Request.body)['predoplata']
    if st =='':
        st = '0'

    predoplata = int(st)
    voplpset = Vidopl.objects.get(pk=int(loads(Request.body)['voplp']))
    
    st = loads(Request.body)['ssbor']
    if st =='':
        st = '0'

    ssbor = int(st)

    psbor = (loads(Request.body)['psbor'])
    customer = (loads(Request.body)['customer'])
    contact = (loads(Request.body)['contact'])
    remark = loads(Request.body)['remark']

    # теперь изменяем данные в базе
    Banket.objects.filter(pk=pk).update(date=dt, 
                                       sum=sum,
                                       vidopl=voplset,
                                       predoplata=predoplata,
                                       vidoplp=voplpset,
                                       ssbor=ssbor,
                                       psbor=psbor,
                                       kolg=kolg,
                                       vidmer=vmerset,
                                       obj=objset,
                                       customer=customer,
                                       contact=contact,
                                       remark=remark
                                       )    

    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def BanketRecAdd (Request):

    # считываем запись из окна создания
    dt = datetime.datetime.strptime((loads(Request.body)['dt']), '%Y-%m-%d').date()
    vmerset = Vidmer.objects.get(pk=int(loads(Request.body)['vmer']))
    objset = Receiver.objects.get(pk=int(loads(Request.body)['obj']))

    st = loads(Request.body)['sum'] 
    if st =='':
        st = '0'

    sum = int(st)

    voplset = Vidopl.objects.get(pk=int(loads(Request.body)['vopl']))

    st = loads(Request.body)['kolg']
    if st =='':
        st = '0'

    kolg = int (st)

    st = loads(Request.body)['predoplata']
    if st =='':
        st = '0'

    predoplata = int(st)
    voplpset = Vidopl.objects.get(pk=int(loads(Request.body)['voplp']))
    
    st = loads(Request.body)['ssbor']
    if st =='':
        st = '0'

    ssbor = int(st)
    
    psbor = (loads(Request.body)['psbor'])
    customer = (loads(Request.body)['customer'])
    contact = (loads(Request.body)['contact'])
    remark = loads(Request.body)['remark']

    # теперь сохраняем данные в базе
    B = Banket(date=dt, 
                                       sum=sum,
                                       vidopl=voplset,
                                       predoplata=predoplata,
                                       vidoplp=voplpset,
                                       ssbor=ssbor,
                                       psbor=psbor,
                                       kolg=kolg,
                                       vidmer=vmerset,
                                       obj=objset,
                                       customer=customer,
                                       contact=contact,
                                       remark=remark,
                                       autor=Request.user.sotr,
                                       datecreated=datetime.datetime.now(),
                                       )    
    B.save()

    return render (Request, 'catalog/accessdenied.html', {'title': ''})

def DN (Num):
    s = '{0:,}'.format(Num).replace(',', ' ')
    return s

def BanketView (Request):
    
    
    # выводим банкеты
    bmas = [] # список банкетов
    omas = [] # список объектов
    vmas = [] # список видов выплат
    mmas = [] # список видов мероприятий

    usr = ''

    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    omas = Receiver.objects.all()
    vmas = Vidopl.objects.all()
    mmas = Vidmer.objects.all()

    begindate = datetime.date.today()
    ddate1 = f'{begindate:%Y-%m-%d}'

    begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')

    b = Banket.objects.filter(date__gte=begindate, active=True).order_by('date')    
    bmas = []; k = 1;            

    for i in b:
        st = {
            'index': k,
            'record': i,
        }

        bmas.append(st) 
        k += 1

    if Request.method == 'POST':
        bform = BanketForm (Request.POST)
        
        if bform.is_valid(): 

            # заполняем данные из формы
            ddate1 = Request.POST['d_date1']

            begindate = datetime.datetime.strptime(ddate1, '%Y-%m-%d')

            b = Banket.objects.filter(date__gte=begindate, active=True).order_by('date')

            bmas = []; k = 1;            

            for i in b:
                st = {
                    'index': k,
                    'record': i,
                    'dt': f'{i.date:%Y-%m-%d}',
                    'vopl': i.vidopl.pk,
                    'voplp': i.vidoplp.pk,
                    'obj': i.obj.pk,
                    'psbor': i.psbor,
                    'date': f'{i.date:%d-%m-%Y}',
                    'dc': f'{i.datecreated:%d-%m-%Y, %H:%M}',
                    'sum_view': DN (i.sum),
                    'predoplata_view': DN (i.predoplata),
                    'ssbor_view': DN (i.ssbor),
                }

                bmas.append(st) 
                k += 1               
        else:
            bform = BanketForm (Request.POST)
    else:
        
        bform =BanketForm (Request.POST)

        b = Banket.objects.filter(date__gte=begindate, active=True).order_by('date')

        bmas = []; k = 1;            

        for i in b:
                st = {
                    'index': k,
                    'record': i,
                    'dt': f'{i.date:%Y-%m-%d}',
                    'vopl': i.vidopl.pk,
                    'voplp': i.vidoplp.pk,
                    'obj': i.obj.pk,
                    'psbor': i.psbor,
                    'date': f'{i.date:%d-%m-%Y}',
                    'dc': f'{i.datecreated:%d-%m-%Y, %H:%M}',
                    'sum_view': DN (i.sum),
                    'predoplata_view': DN (i.predoplata),
                    'ssbor_view': DN (i.ssbor),
                }

                bmas.append(st) 
                k += 1               
        
    return render(Request, 'catalog/banketview.html', {'bdate': ddate1, 'user': Request.user, 
        'menu': mn, 'title': 'Банкеты', 'form': bform, 'bmas': bmas, 'omas': omas, 'vmas': vmas, 'mmas': mmas, 
        })


