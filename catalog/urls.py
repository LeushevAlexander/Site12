from django.urls import path
from .views import HIndex, JobTitleList, TaskList, TaskJobTitleList, AddTasks, SelectTasks, ControlTasks
from .views import About, Tele, QRPayment, QR_status, QRReceipts, SelTask, SelExeZakaz
from .views import AddZakaz, ExeZakaz, AddZakazremark
from .views import AddTabel, EditTabel, AddTabelAdmin, AddDen, EditDen
from .views import LoginUser, logout_user, AccessDenied, WrongDate, ViewMessage, ViewMessageEdit
from .reports import TabelReportSimple, TabelReport, DenReport
from .graphic import AddGraphic, GraphicView, GraphicRecDel, GraphicRecEdit, GraphicRecCopy, GraphSotrInfo
from .banket import BanketView, BanketRecDel, BanketRecEdit, BanketRecAdd
from .chlist import AddChListRec, ChlWork, SetChlTask, ChlControl, ChlUploadImage, ChlTaskInfo
from .chlist import SetChlControlTask, SaveChlControlTaskRem, ChlReportBasic, CreateChlTaskRec, ChlGoWork, ChlGoControl, ChlReportControl, KPITaskReport
from .him import AddZakazHim, ExeZakazHim, AddZakazremarkHim, SelExeZakazHim, NomenHimView, NomenHimRecAdd, NomenHimRecEdit
from .stoplist import StopListView, AddStopList, AddStopListRemark, StopListRecDel, StopListReport
from .den import DenView, DenRecDel, DenRecEdit, DenRecAdd, DenDiagramm
from .stask import STaskView, STaskRecAdd

urlpatterns = [
     path('', HIndex, name='home'), 
     path('jobtitlelist/', JobTitleList, name='JobTitleList'),
     path('tasklist/', TaskList, name='TaskList'),      
     path('taskjobtitlelist/', TaskJobTitleList, name='TaskJobTitleList'),      
     path('about/', About, name='About'),      
     path('addtasks/', AddTasks, name='AddTasks'),      
     path('selecttasks/', SelectTasks, name='SelectTasks'),
     path('controltasks/', ControlTasks, name='ControlTasks'),
     path('qrpayment/', QRPayment, name='QRPayment'),
     path('qrreceipts/', QRReceipts, name='QRReceipts'),
     path('tele/', Tele, name='Tele'),
     path('logout/', logout_user, name='Logout'),
     path('login/', LoginUser.as_view(), name='Login'),
     path('qrgetstatus/<str:order_id>/<str:order_number>/<str:order_sum>/', QR_status, name='qrgetstatus'),
     path('addzakaz/', AddZakaz, name='AddZakaz'),
     path('addzakazremark/', AddZakazremark, name='AddZakazremark'),
     path('exezakaz/', ExeZakaz, name='ExeZakaz'),
     path('addtabel/', AddTabel, name='AddTabel'),
     path('edittabel/', EditTabel, name='EditTabel'),
     path('addtabeladmin/', AddTabelAdmin, name='AddTabelAdmin'),
     path('tabelreportsimple/', TabelReportSimple, name='TabelReportSimple'),
     path('tabelreport/', TabelReport, name='TabelReport'),
     path('accessdenied/', AccessDenied, name='AccessDenied'),      
     path('wrongdate/', WrongDate, name='WrongDate'),
     path('viewmessage/', ViewMessage, name='ViewMessage'),
     path('viewmessageedit/', ViewMessageEdit, name='ViewMessageEdit'),
     path('seltask/<str:task_id>/', SelTask, name='SelTask'),
     path('selexezakaz/<str:param_zakaz>/', SelExeZakaz, name='SelExeZakaz'),
     path('denreport/', DenReport, name='DenReport'),
     path('addchlistrec/', AddChListRec, name='AddChListRec'),
     path('chlwork/', ChlWork, name='ChlWork'),
     path('chlcontrol/', ChlControl, name='ChlControl'),
     path('setchltask/<str:taskpk>/', SetChlTask, name='SelChlTask'),
     path('setchlcontroltask/<str:taskpk>/', SetChlControlTask, name='SelChlControlTask'),
     path('savechlcontroltaskrem/<str:taskpk>/<str:taskrem>/', SaveChlControlTaskRem, name='SaveChlControlTaskRem'),
     path('chlreportbasic/', ChlReportBasic, name='ChlReportBasic'),
     path('createchltaskrec/<str:chlpk>/', CreateChlTaskRec, name='CreateChlTaskRec'),
     path('chlgowork/<str:chlpk>/<str:dt>/', ChlGoWork, name='ChlGoWork'),
     path('chlgocontrol/<str:chlpk>/<str:dt>/', ChlGoControl, name='ChlGoControl'),
     path('chluploadimage/<str:taskpk>/', ChlUploadImage, name='ChlUploadImage'),
     path('chltaskinfo/<str:taskpk>/', ChlTaskInfo, name='ChlTaskInfo'),
     path('chlreportcontrol/', ChlReportControl, name='ChlReportControl'),
     path('kpitaskreport/', KPITaskReport, name='KPITaskReport'),
     path('graphicview/', GraphicView, name='GraphicView'),
     path('addgraphic/', AddGraphic, name='AddGraphic'),
     path('graphicrecdel/<str:gpk>/', GraphicRecDel, name='GraphicRecDel'),
     path('graphicrecedit/<str:gpk>/<str:dt>/<str:t1>/<str:t2>/<str:kol>/<str:pos>/<str:obj>/<str:div>/', GraphicRecEdit, name='GraphicRecEdit'),
     path('graphicreccopy/<str:gpk>/<str:dt>/<str:t1>/<str:t2>/<str:kol>/<str:pos>/<str:obj>/<str:div>/', GraphicRecCopy, name='GraphicRecCopy'),
     path('graphsotrinfo/<str:sid>/<str:d1>/<str:d2>/', GraphSotrInfo, name='GraphSotrInfo'),
     path('banketview/', BanketView, name='BanketView'),
     path('banketrecdel/<str:bpk>/', BanketRecDel, name='BanketRecDel'),
     path('banketrecedit/', BanketRecEdit, name='BanketRecEdit'),
     path('banketrecadd/', BanketRecAdd, name='BanketRecAdd'),
     path('addzakazhim/', AddZakazHim, name='AddZakazHim'),
     path('addzakazremarkhim/', AddZakazremarkHim, name='AddZakazremarkHim'),
     path('exezakazhim/', ExeZakazHim, name='ExeZakazHim'),
     path('selexezakazhim/<str:param_zakaz>/', SelExeZakazHim, name='SelExeZakazHim'),
     path('nomenhimview/', NomenHimView, name='NomenHimView'),
     path('nomenhimrecadd/', NomenHimRecAdd, name='NomenHimRecAdd'),
     path('nomenhimrecedit/', NomenHimRecEdit, name='NomenHimRecEdit'),
     path('stoplistview/', StopListView, name='StopListView'),
     path('addstoplist/', AddStopList, name='AddStopList'),
     path('addstoplistremark/', AddStopListRemark, name='AddStopListRemark'),
     path('stoplistrecdel/<str:slrec>/', StopListRecDel, name='StopListRecDel'),
     path('stoplistreport/', StopListReport, name='StopListReport'),
     path('denview/', DenView, name='DenView'),
     path('denrecdel/<str:bpk>/', DenRecDel, name='DenRecDel'),
     path('denrecedit/', DenRecEdit, name='DenRecEdit'),
     path('denrecadd/', DenRecAdd, name='DenRecAdd'),
     path('dendiagramm/', DenDiagramm, name='DenDiagramm'),
     path('stask/', STaskView, name='STaskView'),
     path('staskrecadd/', STaskRecAdd, name='STaskRecAdd'),

     ]
