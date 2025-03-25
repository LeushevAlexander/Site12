from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from django.urls import reverse_lazy
from django.utils.timezone import now

from django.http import JsonResponse


from .models import TaskJobTitle  
from .models import Task 
from .models import JobTitle
from .models import TaskExe
from .models import CheckListTaskItem
from .models import Nomen, Ei, Source, Receiver, Zakaz, Payment, Podrazd, Vidnach, Sotr, Tabel, Zakazremark, Den, Graphic, Position

import datetime

# Create your views here.
from .forms import AddTasksForm, SelectTasksForm, ControlTasksForm, QRPaymentForm, AddZakazForm, ExeZakazForm, AddZakazremarkForm
from .forms import AddTabelForm, EditTabelForm, AddTabelAdminForm

from .forms import LoginUserForm
from .utils import DataMixin

from .sber import SberQR
from time import sleep
import qrcode
from django.conf import settings
from django.db.models import Q

from django.db import connection

class TaskJobTitleView(View):
    # вывод списка чек листов
    def get(self, request):
        Recs = TaskJobTitle.objects.all()
        return render(request, 'catalog/taskjobtitle.html', {'recs_list':Recs})

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'catalog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def getmenu(request):

    #проверяю, авторизован ли пользователь  

    menu=[]
    # определяю меню исходя из пользователя (полномочий, администратор или нет)
    print(request.user)

    if request.user.is_authenticated:

        #пользователь авторизованный, можно проверять на админ он или нет
        jt=request.user.JT

        if jt.id==1:
            menu = [
          #  {'title': "Список должностей", 'url_name': 'JobTitleList'},
          #  {'title': "Список  чек-листов", 'url_name': 'TaskJobTitleList'},
          #  {'title': "Список  заданий", 'url_name': 'TaskList'},
          #  {'title': "Создание заданий", 'url_name': 'AddTasks'},
            {'title': "Выполнение чек-листа", 'url_name': 'SelectTasks'},
            {'title': "Контроль", 'url_name': 'ControlTasks'},
            {'title': "Оплата QR", 'url_name': 'QRPayment'},
            {'title': "Заявка", 'url_name': 'AddZakaz'},
            {'title': "Выполнение заявки", 'url_name': 'ExeZakaz'},
          #  {'title': "Tel Bot", 'url_name': 'Bot'},
          #  {'title': "О нас...", 'url_name': 'About'},
            ]
        else:
            menu = [
            {'title': "Выполнение", 'url_name': 'SelectTasks'}, # только на выполнение
            {'title': "О нас...", 'url_name': 'About'},  
            ]      

    else:
          menu = [
           {'title': "О нас...", 'url_name': 'About'},  
        ]      
          
    return menu        

def logout_user(request):
    logout(request)
    return redirect('Login') 

def HIndex(Request):

    mn=getmenu(Request)
    context = {
        'menu': mn,
        'title': 'Главная страница'
    }

    return render (Request, 'catalog/index.html', context)

def About(Request):

    mn=getmenu(Request)
    context = {
        'menu': mn,
        'title': 'О нас...'
    }    
    return render (Request, 'catalog/about.html', context)

def AccessDenied(Request):

    mn=getmenu(Request)
    return render (Request, 'catalog/accessdenied.html', {'menu': mn, 'title': 'Доступ запрещен....'})

def WrongDate(Request):

    mn=getmenu(Request)
    return render (Request, 'catalog/accessdenied.html', {'menu': mn, 'title': 'Неверная дата....'})

def ViewMessage(Request):

    mn=getmenu(Request)
    return render (Request, 'catalog/accessdenied.html', {'menu': mn, 'title': 'Рабочий день создан !' })

def ViewMessageEdit(Request):

    mn=getmenu(Request)
    return render (Request, 'catalog/accessdenied.html', {'menu': mn, 'title': 'Рабочий день изменен !' })

#def Login(Request):
#    return render (Request, 'catalog/login.html', {'menu': menu, 'title': 'Авторизация пользователя...'})

def JobTitleList(Request):
    mn=getmenu(Request)
    Recs_list = JobTitle.objects.all()
    return render (Request, 'catalog/jobtitlelist.html', {'Recs_list': Recs_list, 'menu': mn, 'title': 'Список должностей...'})

def TaskList(Request):
    mn=getmenu(Request)
    tasks_list = Task.objects.all()
    return render(Request, 'catalog/tasklist.html', {'tasks_list': tasks_list, 'menu': mn, 'title':'Список заданий...'})

def TaskJobTitleList(Request):
    rec = TaskJobTitle.objects.all()
    mn=getmenu(Request)
    return render (Request, 'catalog/taskjobtitlelist.html', {'rec': rec, 'menu': mn, 'title': 'Список чек-листов...'})

def AddTasks(Request):

    mn = getmenu(Request)

    if Request.method == 'POST':
        form = AddTasksForm(Request.POST)
        if form.is_valid():
            
            p = TaskJobTitle.objects.all() #выборка по чек листам
            for k in p:
                #J = form.cleaned_data.get('jt')
                #TJ = form.cleaned_data.get('tjt')

                #w = CheckListTaskItem.objects.all()
                w = CheckListTaskItem.objects.filter(cheklistlink=k)
                for v in w:                    
                    t = TaskExe(date=form.cleaned_data.get('date_creation'), jobtitlelink=k.jobtitle, taskjobtitlelink=k, tasklink=v.tasklink, time_control=v.time_control, order=v.order)                
                    t.save()                
                
            #TaskExe.objects.create(date=form.cleaned_data.get('date_creation'), jobtitlelink=J, taskjobtitle=k.id)   
            #J = form.cleaned_data.get('jt')
            # нужно добавить записи в таблицу Task Exe
            #TaskExe.objects.create(date=form.cleaned_data.get('date_creation'), jobtitlelink=J)
            
            return redirect('home')
    
    form = AddTasksForm ()    
    return render(Request, 'catalog/addtasks.html', {'form': form, 'menu': mn, 'title': 'Добавление заданий на день'})

def SelectTasks(Request):

    usr=''

    mn=getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 


    #clist = TaskJobTitle.objects.all() # Список чек листов
    #определяю задания на день, сначала - все
    #tlist = TaskExe.objects.all() date=datetime.date.today    
    jt=Request.user.JT;    
    dt = datetime.date.today()

    if jt.id == 1:
        clist = TaskJobTitle.objects.all() # Список чек листов весь полностью
    else:
        clist = TaskJobTitle.objects.filter(jobtitle=jt) # только выделенная должность   
 
    tlist = TaskExe.objects.filter(status=False, date=dt)

    if Request.method == 'POST':

        jt=Request.user.JT;

        choice_id = int(Request.POST['choise'])

        formselect = SelectTasksForm(Request.POST)
        if formselect.is_valid(): 

            #ts = TaskExe(id=choice_id)
            #ts.status=True
            #ts.save()

            # устанавливаем время Execute и пользователя
            us=Request.user.username
            TaskExe.objects.filter(id=choice_id).update(status=True, user_exe=us, time_exe=datetime.datetime.now())
    
            return redirect('SelectTasks')
    
    formselect = SelectTasksForm()        
    
    return render(Request, 'catalog/selecttasks.html', {'clist': clist, 'form': formselect, 'loginuser': usr, 'menu': mn, 'tlist': tlist, 'title': 'Выполнение заданий на день.'})


def SelTask (Request, task_id):
    k =0
    t=int(task_id)
    us=Request.user.username
    r = TaskExe.objects.filter(id=t).update(status=True, user_exe=us, time_exe=datetime.datetime.now())
    return 

def ControlTasks(Request):

    usr=''
    mn = getmenu(Request)
    clist = TaskJobTitle.objects.all() # Список чек листов

    #определяю задания на день, сначала - все
    #tlist = TaskExe.objects.all() date=datetime.date.today    
    dt = datetime.date.today()
    tlist = TaskExe.objects.filter(date=dt) # все задания по дате
 
    if Request.method == 'POST':

        #choice_id = int(Request.POST['choise'])

        formcontrol = ControlTasksForm(Request.POST)
        if formcontrol.is_valid(): 

            #обновляем форму исходя из данных
            dt = formcontrol.cleaned_data.get('date_control')
            tjt = formcontrol.cleaned_data.get('tjt')
            if not tjt is None:
                #tjt определен
                tlist = TaskExe.objects.filter(date=dt, taskjobtitlelink=tjt) # все задания по дате
                clist = TaskJobTitle.objects.filter(id=tjt.id)
            else:
                #tjt не определен, выбираем все
                tlist = TaskExe.objects.filter(date=dt)
                clist = TaskJobTitle.objects.all()    
    else:    
        formcontrol = ControlTasksForm()        
    
    return render(Request, 'catalog/controltasks.html', {'clist': clist, 'form': formcontrol, 'loginuser': usr, 'menu': mn, 'tlist': tlist, 'title': 'Контроль заданий.'})

#Возврат json по запросу из приложения Bot
def Tele(request):

    # ts=JobTitle.objects.all()    
    # #делаю json массив со списком в из таблицы
    # t=[]
    # for i in ts:
    
    #     st={'name': i.jobtitlename, 'id': i.id}
    #     t.append(st)    

    t=[]
    dt=datetime.date.today()
    
    clist = TaskJobTitle.objects.all() # Список чек листов весь полностью необходимо для создания ключа по чек листу

    for i in clist:
        
        #st={'clist': i.name, 'clist_id': i.id}

        k = 0  # наименование чек листа не вставлено
        z=[] #список задач

        #делаем выборку по задачам
        tlist = TaskExe.objects.filter(date=dt, taskjobtitlelink=i, status=0) # все задания по дате и чек листу
        for l in tlist:

            #проверяю задачу на время
            now=datetime.datetime.now()
            tc=l.time_control

            today_control=now.replace(hour=tc.hour, minute=tc.minute, second=0)

            if now > today_control:  #время просрочено, надо сообщить                
                #вставляю данные по невыполным задачам
                zs={'task': l.tasklink.taskname, 'time_control': l.time_control, 'task_exe_id': l.id}
                z.append(zs)
            
        if len(z)>0: #нашлись задачи которые не выполнены
            st={'clist_id': i.id, 'clist': i.name, 'task_exe': z}
            t.append(st)

    return JsonResponse({'table': t})   

def QR_status(request, order_id, order_number, order_sum):
    sber_qr = SberQR(
        settings.MEMBER_ID, 
        settings.TID,   
        settings.ID_GR,
        settings.CLIENT_ID,  
        settings.CLIENT_SECRET, 
        settings.PKCS12_FILENAME, 
        settings.PKCS12_PASSWORD
    )
    
    # data_status = sber_qr.status(request.GET["order_id"] , request.GET[''])
    data_status = sber_qr.status(order_id, order_number, order_sum)
    return JsonResponse(data_status)   


def QRPayment(Request):
        
    img = '' # имидж qr кода
    status = 0 # status = 0 выводим форму с вводом суммы, синаче выводим форму с QR кодом

    mn = getmenu(Request)

    if Request.method == 'POST':
        formcontrol = QRPaymentForm(Request.POST)
        if formcontrol.is_valid():
            # обрабатываем событие для формирования QR кода
            
            sm = formcontrol.cleaned_data.get('QR_sum') #сумма

            sm = sm.replace(',', '.')

            sm_opl = sm # для вывода суммы оплаты

            sm = float(sm)
            sm = int (sm * 100)
            
            sber_qr = SberQR(
                settings.MEMBER_ID, 
                settings.TID,   
                settings.ID_GR,
                settings.CLIENT_ID,  
                settings.CLIENT_SECRET, 
                settings.PKCS12_FILENAME, 
                settings.PKCS12_PASSWORD
            )
            
            data = sber_qr.creation('Оплата заказа', sm, is_sbp=True)
            print(data)
            #qrcode.make(data['order_form_url']).save("qr.png")
            #qrcode.make(data['order_form_url']).save('/home/site1/static/QR/CODE_' + data['order_number'] + '.png') #!!! для Ubuntu
            qrcode.make(data['order_form_url']).save('static/QR/CODE_' + data['order_number'] + '.png')

            #теперь необходимо вывести страницу с генерированным QR кодом
            img = '/QR/CODE_' + data['order_number'] + '.png'
            # img = '/QR/CODE_' + data['order_number'] + '.png'

            status = 1

            # while True:
                        #     sleep(1)
            #     data_status = sber_qr.status(data['order_id'], data['order_number'])
            #     print(data_status)

            return render(Request, 'catalog/qrpayment.html', {'form': formcontrol, 'menu': mn, 
                'title': 'Оплата СПБ QR', 'image': img, 'status': status, 
                'order_sum': sm_opl, 'order_id': data['order_id'], 'order_number': data['order_number']})
                

            #     if data_status['order_state'] == 'PAID':
            #         print('Оплачено')
            #         break

    else:
        formcontrol = QRPaymentForm()

    return render(Request, 'catalog/qrpayment.html', {'form': formcontrol, 'menu': mn, 
        'title': 'Оплата СПБ QR', 'image': img, 'status': status, 'order_sum': ''})

def QRReceipts(Request):

    # если не авторизован, то выход
    mn=getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login')     

    # выводим список поступлений по QR коду
    qrlist = Payment.objects.order_by('-date') # Список поступлений по чек листу с сортировкой по -дате 
    #qrlist = QRPayment.objects.all() # Список поступлений по чек листу с сортировкой по -дате 

    return render(Request, 'catalog/qrreceipts.html', {'menu': mn, 'title': 'Перечень поступлений по QR СБП.',
                         'qrlist': qrlist, })    

def AddZakaz(Request):

    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    sstr = '' # строка поиска

    nomenlist = Nomen.objects.order_by('name')  # Список номенклатуры
    elist = Ei.objects.all() # Список единиц измерения
    slist = Source.objects.all() # Список источников (баз)
    rlist = Receiver.objects.all() # Список мест объектов производства / по умолчанию - тот, который в пользователе

    # nmlist = []
    # for n in nomenlist:
    #     st = {
    #         'name:' :n.name,
    #         'ei': n.ei,
    #         'id': n.pk,
    #         'image': str(n.img),
    #         'desc': str(n.description)
    #     }

    #     print (n.description)
    #     nmlist.append(n)

    dt = datetime.date.today()
    zakazdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':

        formzakaz = AddZakazForm(Request.POST)
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
                    nomenlist = Nomen.objects.filter(name__icontains=searchstring).order_by('name')  # Список номенклатуры фильтрую по строке
                    nlist = Nomen.objects.filter(name__icontains=searchstring).order_by('name')
                    sstr = searchstring
                else:
                    nlist = Nomen.objects.all().order_by('name')
                    nomenlist = Nomen.objects.all().order_by('name')

            if ch=='create':
                
                # надо создать, в зависимости от фильтра searchstring
                if searchstring != '':
                    # надо отфильтровать по строке
                    searchstring=searchstring.upper()
                    nomenlist = Nomen.objects.filter(name__icontains=searchstring).order_by('name')  # Список номенклатуры фильтрую по строке
                    nlist = Nomen.objects.filter(name__icontains=searchstring).order_by('name')
                    sstr = searchstring
                else:
                    nlist = Nomen.objects.all().order_by('name')
                    nomenlist = Nomen.objects.all().order_by('name')

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
                                
                    z =Zakaz(date=zdate, source_link=sr, receiver_link=rc, nomen_link=nm, creator=Request.user.username, 
                            cost=cs, kol=kl, ei_link=e, status=0, time_create=tm)                
                    z.save()
            
                #теперь надо перенаправить на страницу сообщения о создании заявки по следующим позициям
                if len(mas) > 0:
                    return render(Request, 'catalog/zakazcreated.html', {'nlist': mas, 'loginuser': usr, 
                    'menu': mn, 'title': 'Заявка создана.', 'date_zakaz': zdate,   
                    'elist': elist, 'slist': slist, 'rlist': rlist, })
                    
    else:    
        formzakaz = AddZakazForm()        

    return render(Request, 'catalog/addzakaz.html', {'nlist': nomenlist, 'form': formzakaz, 
        'loginuser': usr, 'menu': mn, 'title': 'Создание заказа.', 
        'elist': elist, 'slist': slist, 'rlist': rlist, 'date_zakaz': zakazdate, 'zstr': sstr,
        })

def AddZakazremark(Request):
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
        
        formremark = AddZakazremarkForm(Request.POST)
        if formremark.is_valid(): 
           
            # нажали кнопку создания заявки, необходимо ее обработать ))
            textremark = Request.POST['textremark']                                
            r =Zakazremark(date=dt, creator=usr.username, remark=textremark, status=False, time_create=dt)
            r.save()
            
            #теперь надо перенаправить на страницу сообщения о создании табеля по следующим позициям
            tdate=f'{dt:%d-%m-%Y}'
            return render(Request, 'catalog/zakazremarkcreated.html', {'menu': mn, 'title': 'Комментарий сохранен.', 
                        'date_remark': tdate, 'textremark': textremark, 'creator': usr.username, })
           
    else:
        formremark = AddZakazremarkForm()

    return render(Request, 'catalog/addzakazremark.html', {'remark': '', 'form': formremark, 
        'menu': mn, 'title': 'Создание комментария.', })


def ExeZakaz(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 
    
    rm = []

    # заполняю комментарии к заявкам, выделенным цветом
    rmlist = Zakazremark.objects.filter(status=False)

    # Вывожу список продуктов которые в заявке
    # где status < 2 и date <= дате на экране
    
    # zlist = Zakaz.objects.filter(Q(status=0)|Q(status=1))
    zlist = Zakaz.objects.filter(Q(status=0)|Q(status=1)).order_by('nomen_link__name')
    # zlist = Zakaz.objects.filter(status=0).order_by('nomen_link__name')

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

        exezakaz = ExeZakazForm(Request.POST)

        if exezakaz.is_valid(): 
            # обрабатываю нажатие кнопки
            choice_str = Request.POST['choise']

            # проверяем ремарка это или нет
            q=choice_str[:2]
            if q=='rm': # это ремарка, надо ее погасить и не трогать номенклатуру
                rpk = choice_str[2:]
                rpk = int(rpk)

                Zakazremark.objects.filter(pk=rpk, status=False).update(status=True, maker=Request.user.username, time_make=datetime.datetime.now())
                return redirect('ExeZakaz')                
            
            # Иначе
            # Бомбим нажатие по кнопке номенклатуры
            id_list=choice_str.split(sep=';')
            nomen_id=int(id_list[0])
            source_id=int(id_list[1])
            sts=int(id_list[2])

            nomen_obj = Nomen.objects.get(id=nomen_id)
            source_obj=Source.objects.get(id=source_id)

            # теперь надо сделать update в зависимости от статуса заказа
            if sts==0:
                #устанавливаем флаг 1 (значит заказ взят, но не доставлен)
                Zakaz.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=0).update(status=1, maker=Request.user.username, time_make=datetime.datetime.now())
                return redirect('ExeZakaz')
            
            elif sts==1:
                #устанавливаем флаг 2 (значит заказ и взят и доставлен)
                Zakaz.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=1).update(status=2, deliver=Request.user.username, time_deliv=datetime.datetime.now())
                return redirect('ExeZakaz')

    exezakaz = ExeZakazForm()                
    return render(Request, 'catalog/exezakaz.html', {'nlist': mz, 'form': exezakaz, 'loginuser': usr, 
                        'menu': mn, 'title': 'Заявка на продукты.', 'remark': rmlist, })

def SelExeZakaz (Request, param_zakaz):

    # Бомбим нажатие по кнопке номенклатуры
    id_list=param_zakaz.split(sep=';')
    nomen_id=int(id_list[0])
    source_id=int(id_list[1])
    sts=int(id_list[2])

    nomen_obj = Nomen.objects.get(id=nomen_id)
    source_obj=Source.objects.get(id=source_id)

    # теперь надо сделать update в зависимости от статуса заказа
    if sts==0:
        #устанавливаем флаг 1 (значит заказ взят, но не доставлен)
        Zakaz.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=0).update(status=1, maker=Request.user.username, time_make=datetime.datetime.now())
            
    elif sts==1:
        #устанавливаем флаг 2 (значит заказ и взят и доставлен)
        Zakaz.objects.filter(nomen_link=nomen_obj, source_link=source_obj, status=1).update(status=2, deliver=Request.user.username, time_deliv=datetime.datetime.now())

    return render (Request, 'catalog/accessdenied.html', {'title': 'Отметка в заявке...'})

def AddTabel(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_Tabel != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    usr = Request.user
    t_div = usr.sotr.div # подразделение такое
    t_obj = usr.sotr.obj # объект по умолчанию

    #slist = Sotr.objects.filter(div=pd, active=True).order_by('name')  # Список сотрудников, отбираем по подразделению и активности
    slist = Sotr.objects.filter(active=True).order_by('name')  # Список всех сотрудников
    omas = Receiver.objects.all() # Список объектов производства / по умолчанию - тот, который в пользователе
    dmas = Podrazd.objects.all() # Список подразделений / по умолчанию - тот, который в пользователе
    sstr = ''

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':
        
        mas = []

        formtabel = AddTabelForm(Request.POST)
        if formtabel.is_valid(): 

            # проверяем какую кнопку нажали
            # определяю, нажата ли клавиша поиск...
            td = Request.POST['tabel_date']
            tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

            # определяем объект
            t_obj = Request.POST['ob_field']
            t_obj = Receiver.objects.get(id=t_obj)

            # определяем подразделение
            t_div = Request.POST['div_field']
            t_div = Podrazd.objects.get(id=t_div)
            
            #searchstring = Request.POST['searchstring']
            
            ch = Request.POST['choise']

            #if ch == 'search':

                # нажата клавиша поиск, выполняем команду поиска, обновляем, ничего не создаем                
            #    if searchstring != '':
                    # надо отфильтровать по строке
#                    searchstring=searchstring.upper()
            #        slist = Sotr.objects.filter(name__icontains=searchstring,active=True).order_by('name')  # Список менюсотрудников фильтрую по строке
            #        sstr = searchstring
            #    else:
            #        slist = Sotr.objects.filter(active=True).order_by('name')

            #    tdate = td

            if ch == 'create':

                # нажали кнопку создания табеля, необходимо ее обработать ))
                # и создать записи по сотрудникам )))
                td = Request.POST['tabel_date']
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

                # определяем объект
                t_obj = Request.POST['ob_field']
                t_obj = Receiver.objects.get(id=t_obj)

                # определяем подразделение
                t_div = Request.POST['div_field']
                t_div = Podrazd.objects.get(id=t_div)

                td1 = datetime.timedelta(days=1)
                # делаю проверку, дату можно только сегодняшнюю и вчерашнюю

                #if (tdate.date() < (datetime.datetime.now().date()-td1)) and (tdate.date() > datetime.datetime.now().date()):
                if (tdate.date() < (datetime.datetime.now().date()-td1)) or (tdate.date() > datetime.datetime.now().date()):
                    # сообщаю, что дата не вписывается в диапазон, и выхожу
                    return redirect('WrongDate') 

                # надо найти как то количество, которое я поставил ))
                for n in slist:
                    st ='sotr' + str(n.id)
                    kol = Request.POST[st]
                    kol = kol.replace(',', '.')

                    t1 = 'sotr_t1' + str(n.id)
                    t2 = 'sotr_t2' + str(n.id)
                    t1 = Request.POST[t1]
                    t2 = Request.POST[t2]

                    if len(kol) > 0:
                                                            
                        kol = float(kol)
                        if kol != 0:
                        
                            #вставляю в массив для табеля
                            rec = {
                            'sotr': n,
                            'kol': kol,
                            't1': t1,
                            't2': t2,
                            'f': 1,    # Флаг = 1, значит надо отображать как добавленный в табель, если 0 тогда как существующий
                            }                        

                            mas.append(rec)
                        
                # пора формировать запись в базе
                for i in mas:
                    # добавяю запись в таблицу табеля
                    sot=i['sotr']
                    kl=i['kol']
                    tt1=i['t1']
                    tt2=i['t2']

                    e=sot.ei  #ei= 'Час'
                    v=Vidnach.objects.get(pk=1) # Vidnach = 'Табель'

                    # если права админские, то сразу вставляем запись 
                    if Request.user.A_TabelAdmin == True:
                        t =Tabel(date=tdate, sotr=sot, ei=sot.ei, vidnach=v, kol=kl, stavka=float(sot.stavka), sum=kl*float(sot.stavka),
                            div=t_div, obj=t_obj, avtor=usr.username, datecreated=datetime.datetime.now(), t1=tt1, t2=tt2)
                         
                        t.save()
                    else:
                        # Нужно проверить, есть ли уже записи по табелю в этот день по этому сотруднику
                        # Если нет, тогда создаем запись, если есть то ставим флаг вывода = 0 и не создаем запись
                        tl = Tabel.objects.filter(date=tdate, sotr=sot, vidnach=v, div=t_div, obj=t_obj) # список записей в табеле
                
                        if len(tl) == 0:                                
                            t =Tabel(date=tdate, sotr=sot, ei=sot.ei, vidnach=v, kol=kl, stavka=float(sot.stavka), sum=kl*float(sot.stavka),
                                div=t_div, obj=t_obj, avtor=usr.username, datecreated=datetime.datetime.now(), t1=tt1, t2=tt2)
                         
                            t.save()
                        else:
                            i['f'] = 0
            
                #теперь надо перенаправить на страницу сообщения о создании табеля по следующим позициям
                if len(mas) > 0:
                    tdate=f'{tdate:%d-%m-%Y}'
                    return render(Request, 'catalog/tabelcreated.html', {'slist': mas,  
                        'menu': mn, 'title': 'Табель сохранен.', 'date_tabel': tdate, 'obj': t_obj, 'div': t_div, })
           
    else:
        formtabel = AddTabelForm()

    return render(Request, 'catalog/addtabel.html', {'slist': slist, 'form': formtabel, 'omas': omas, 'dmas': dmas,
        'menu': mn, 'title': 'Создание табеля.', 'obj': t_obj, 'div': t_div, 'date_tabel': tdate, 'sstr': sstr,
        })

def EditTabel(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_TabelAdmin != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'
    usr = Request.user
    rlist = Receiver.objects.all() # Список объектов производства / по умолчанию - тот, который в пользователе

    # Делаю список сотрудников в табеле для редактирования данных
    tl = Tabel.objects.filter(date=tdate) # список записей в табеле за эту дату
    
    if Request.method == 'POST':
        
        formtabel = EditTabelForm(Request.POST)
        if formtabel.is_valid(): 
           
            # нажали кнопку, надо определить, что нажали
            ch = Request.POST['choise']
            
            if ch == 'reload':  # считываем дату и обновляем страничку

                td = Request.POST['tabel_date']                
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
                tl = Tabel.objects.filter(date=tdate) # список записей в табеле за эту дату
                tdate = f'{tdate:%Y-%m-%d}'
            
            if ch == 'update': # Сохраняем изменения в базе

                td = Request.POST['tabel_date']                
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
                tl = Tabel.objects.filter(date=tdate) # список записей в табеле за эту дату
                tdate = f'{tdate:%Y-%m-%d}'

                for n in tl:
                    # проверяю на изменения
                    st = 'sotr_iz' + str(n.id)
                    if st in Request.POST: # изменения есть, надо их записать
                        # помимо записи измененных полей, надо сделать пересчет суммы
                        st = 'sotr' + str(n.id)
                        kol = Request.POST[st]
                        kol = kol.replace(',', '.')

                        t1 = 'sotr_t1' + str(n.id); t1 = Request.POST[t1]
                        t2 = 'sotr_t2' + str(n.id); t2 = Request.POST[t2]

                        kol = float(kol)
                        sm = n.stavka * kol

                        # Обновляю данные в базе
                        Tabel.objects.filter(pk=n.id).update(kol=kol, t1=t1, t2=t2, sum=sm)

                    # проверяю на удаление
                    st = 'sotr_del' + str(n.id)
                    if st in Request.POST: # удаление есть, надо удалить
                        Tabel.objects.filter(pk=n.id).delete()

                # делаем reload
                td = Request.POST['tabel_date']                
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
                tl = Tabel.objects.filter(date=tdate) # список записей в табеле за эту дату
                tdate = f'{tdate:%Y-%m-%d}'
           
    else:
        formtabel = EditTabelForm()

    return render(Request, 'catalog/edittabel.html', {'tl': tl, 'form': formtabel, 
        'menu': mn, 'title': 'Изменение табеля.', 'date_tabel': tdate,
        })

def AddTabelAdmin(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_TabelAdmin != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    usr = Request.user

    slist = Sotr.objects.filter(active=True).order_by('name')  # Список сотрудников, отбираем по активности
    vnach = Vidnach.objects.all()

    vmas = []

    # st={'name': '[Все]', 'id': 0}
    # vmas.append(st)

    for w in vnach:
        st={'name': w.name, 'id': w.pk}
        vmas.append(st)

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'

    if Request.method == 'POST':
        
        mas = []

        formtabeladmin = AddTabelAdminForm(Request.POST)
        if formtabeladmin.is_valid(): 
           
            # нажали кнопку создания табеля, необходимо ее обработать ))
            # и создать записи по сотрудникам )))
            td = Request.POST['tabel_date']
            vnch = Request.POST['vnach_field']
            tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

            nch = Vidnach.objects.get(pk=vnch)

            # надо найти как то  количество, которое я поставил ))
            for n in slist:
                st ='sotr' + str(n.id)
                kol = Request.POST[st]
                kol = kol.replace(',', '.')

                if len(kol) > 0:
                                                            
                    kol = float(kol)
                    if kol != 0:
                        
                        #вставляю в массив для заявки
                        rec = {
                            'sotr': n,
                            'kol': kol,
                        }                        
                        
                        mas.append(rec)
                        
            # пора формировать запись в базе
            # kol уже не количество а сумма !!!!

            for i in mas:
                # добавяю запись в таблицу начислений по табелю
                sot=i['sotr']
                kl=i['kol']

                e=sot.ei  #ei= 'Час'
                                
                t =Tabel(date=tdate, sotr=sot, ei=sot.ei, vidnach=nch, kol=1, stavka=sot.stavka, sum=kl,
                         div=sot.div, obj=sot.obj, avtor=usr.username, datecreated=dt)
                         
                t.save()
            
            #теперь надо перенаправить на страницу сообщения о создании начислений по следующим позициям
            if len(mas) > 0:
                tdate=f'{tdate:%d-%m-%Y}'
                return render(Request, 'catalog/tabelcreatedadmin.html', {'slist': mas,  
                    'menu': mn, 'title': 'Табель (Админ) сохранен.', 'date_tabel': tdate, 
                    'vnach': nch.name, })
           
    else:
        formtabeladmin = AddTabelAdminForm()

    return render(Request, 'catalog/addtabeladmin.html', {'slist': slist, 'form': formtabeladmin, 
        'menu': mn, 'title': 'Создание табеля (Админ).', 'vnach': vmas, 
        'date_tabel': tdate,
        })


def AddDen(Request):
    k = 0
    # usr = ''
    # mn = getmenu(Request)

    # if Request.user.is_authenticated == False:
    #     # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
    #     return redirect('Login') 

    # if Request.user.A_Den != True:
    #     # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
    #     return redirect('AccessDenied') 

    # usr = Request.user

    # dt = datetime.date.today()
    # tdate = f'{dt:%Y-%m-%d}'
    # rlist = Receiver.objects.all() # Список объектов реализации 

    # if Request.method == 'POST':
        
    #     formden = AddDenForm(Request.POST)
    #     if formden.is_valid(): 
           
    #         # нажали кнопку создания дня, необходимо ее обработать ))
    #         # получаю данные из рабочего дня
    #         # и создаю запись

    #         td = Request.POST['den_date']
    #         tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

    #         obj = Request.POST['obj']
    #         obj = Receiver.objects.get(pk=obj)
            
    #         vnal = Request.POST['vnal']
    #         vnal = vnal.replace(',', '.')
    #         if vnal == '': vnal = 0 
    #         else: vnal = float(vnal)

    #         vbnal = Request.POST['vbnal']
    #         vbnal = vbnal.replace(',', '.')
    #         if vbnal == '': vbnal = 0 
    #         else: vbnal = float(vbnal)

    #         vbs = Request.POST['vbs']
    #         vbs = vbs.replace(',', '.')
    #         if vbs == '': vbs = 0 
    #         else: vbs = float(vbs)

    #         vpp = Request.POST['vpp']
    #         vpp = vpp.replace(',', '.')
    #         if vpp == '': vpp = 0 
    #         else: vpp = float(vpp)
         
    #         vpr = Request.POST['vpr']
    #         vpr = vpr.replace(',', '.')
    #         if vpr == '': vpr = 0 
    #         else: vpr = float(vpr)

    #         vsert = Request.POST['vsert']
    #         vsert = vsert.replace(',', '.')
    #         if vsert == '': vsert = 0 
    #         else: vsert = float(vsert)

    #         vbar = Request.POST['vbar']
    #         vbar = vbar.replace(',', '.')
    #         if vbar == '': vbar = 0 
    #         else: vbar = float(vbar)

    #         vkuh = Request.POST['vkuh']
    #         vkuh = vkuh.replace(',', '.')
    #         if vkuh == '': vkuh = 0 
    #         else: vkuh = float(vkuh)

    #         chn = Request.POST['chn']
    #         chn = chn.replace(',', '.')
    #         if chn == '': chn = 0 
    #         else: chn = float(chn)

    #         chbn = Request.POST['chbn']
    #         chbn = chbn.replace(',', '.')
    #         if chbn == '': chbn = 0 
    #         else: chbn = float(chbn)
            
    #         kolg = Request.POST['kolg']
    #         kolg = kolg.replace(',', '.')
    #         if kolg == '': kolg = 0 
    #         else: kolg = float(kolg)

    #         # сохраняю запись
    #         t = Den(date=tdate, vnal=vnal, vbnal=vbnal, vbc=vbs, vpp=vpp, vpr=vpr, vsert=vsert, vb=vbar, vk=vkuh,
    #                 chn=chn, chbn=chbn, kolg=kolg, obj=obj, avtor=usr.username, datecreated=tdate.date())                         
    #         t.save()

    #         # сообщаю что документ сохранен
    #         return redirect('ViewMessage')        

    # else:
    #     formden = AddDenForm()

    # return render(Request, 'catalog/addden.html', {'form': formden, 'rlist': rlist,
    #     'menu': mn, 'title': 'Создание рабочего дня.', 'date_den': tdate,
    #     })


def EditDen(Request):
    usr = ''
    mn = getmenu(Request)

    if Request.user.is_authenticated == False:
        # пользователь у нас не авторизован, поэтому необходимо идти на страницу авторизации
        return redirect('Login') 

    if Request.user.A_Den != True:
        # у пользователя доступ запрещен нас не авторизован, поэтому необходимо идти на 
        return redirect('AccessDenied') 

    usr = Request.user

    dt = datetime.date.today()
    tdate = f'{dt:%Y-%m-%d}'
    rlist = Receiver.objects.all() # Список объектов реализации (в нашем случае кафе)

    vnal = 0; vbnal = 0; vbs = 0; vpp = 0; vpr = 0; vsert = 0; vbar = 0; vkuh = 0; chn = 0; chbn = 0; kolg = 0
    editdata = { 
        'vnal': vnal, 'vbnal': vbnal, 'vbs': vbs, 'vpp': vpp, 'vpr': vpr, 'vsert': vsert,
        'vbar': vbar, 'vkuh': vkuh, 'chn': chn, 'chbn': chbn, 'kolg': kolg,
    }

    if Request.method == 'POST':
        
        formden = EditDenForm(Request.POST)
        if formden.is_valid(): 
           
            # нажали кнопку в форме изменения дня дня, необходимо ее обработать ))
            # сначала определяю, что это за кноапка, заполнить или сохранить
            # получаю данные из рабочего дня
            # и создаю запись

            ch = Request.POST['choise']

            if ch == 'fill':
                # Нажата клавиша Заполнить, заполняем поля данными
                td = Request.POST['den_date']
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')
                obj = Request.POST['obj']
                obj = Receiver.objects.get(pk=obj)
                
                # определяю max id записи по этим параметрам и считываю данные в переменные
                dlist = Den.objects.filter(date=tdate, obj=obj)  # отбираем по параметрам
                
                for d in dlist:
                    # заполняю параметры для открытия окна
                    editdata = { 
                            'vnal': d.vnal, 'vbnal': d.vbnal, 'vbs': d.vbc, 'vpp': d.vpp, 'vpr': d.vpr, 
                            'vsert': d.vsert, 'vbar': d.vb, 'vkuh': d.vk, 'chn': d.chn, 
                            'chbn': d.chbn, 'kolg': d.kolg, 'obj': obj,
                        }
                tdate = f'{tdate:%Y-%m-%d}'
                formden = EditDenForm()


            if ch == 'edit':
                # нажата клавиша edit, надо обновить данные за день по указанному объекту

                td = Request.POST['den_date']
                tdate = datetime.datetime.strptime(td, '%Y-%m-%d')

                obj = Request.POST['obj']
                obj = Receiver.objects.get(pk=obj)
            
                vnal = Request.POST['vnal']
                vnal = vnal.replace(',', '.')
                if vnal == '': vnal = 0 
                else: vnal = float(vnal)

                vbnal = Request.POST['vbnal']
                vbnal = vbnal.replace(',', '.')
                if vbnal == '': vbnal = 0 
                else: vbnal = float(vbnal)

                vbs = Request.POST['vbs']
                vbs = vbs.replace(',', '.')
                if vbs == '': vbs = 0 
                else: vbs = float(vbs)

                vpp = Request.POST['vpp']
                vpp = vpp.replace(',', '.')
                if vpp == '': vpp = 0 
                else: vpp = float(vpp)
         
                vpr = Request.POST['vpr']
                vpr = vpr.replace(',', '.')
                if vpr == '': vpr = 0 
                else: vpr = float(vpr)

                vsert = Request.POST['vsert']
                vsert = vsert.replace(',', '.')
                if vsert == '': vsert = 0 
                else: vsert = float(vsert)

                vbar = Request.POST['vbar']
                vbar = vbar.replace(',', '.')
                if vbar == '': vbar = 0 
                else: vbar = float(vbar)

                vkuh = Request.POST['vkuh']
                vkuh = vkuh.replace(',', '.')
                if vkuh == '': vkuh = 0 
                else: vkuh = float(vkuh)

                chn = Request.POST['chn']
                chn = chn.replace(',', '.')
                if chn == '': chn = 0 
                else: chn = float(chn)

                chbn = Request.POST['chbn']
                chbn = chbn.replace(',', '.')
                if chbn == '': chbn = 0 
                else: chbn = float(chbn)
            
                kolg = Request.POST['kolg']
                kolg = kolg.replace(',', '.')
                if kolg == '': kolg = 0 
                else: kolg = float(kolg)

                #обновляю запись
                t = Den.objects.filter(date=tdate, obj=obj).update(vnal=vnal, vbnal=vbnal, vbc=vbs, vpp=vpp, vpr=vpr, vsert=vsert, vb=vbar, vk=vkuh,
                        chn=chn, chbn=chbn, kolg=kolg, obj=obj, avtor=usr.username, datecreated=tdate.date())

                # сообщаю что документ сохранен
                return redirect('ViewMessageEdit')        

    else:
        formden = EditDenForm()

    return render(Request, 'catalog/editden.html', {'form': formden, 'rlist': rlist,
        'menu': mn, 'title': 'Изменение рабочего дня.', 'date_den': tdate, 'editdata': editdata,
        })

