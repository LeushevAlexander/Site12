from django import forms
from .models import JobTitle, TaskJobTitle, TaskExe

from .models import Source, Receiver


from django.contrib.auth.forms import AuthenticationForm
import datetime, array

class AddTasksForm(forms.Form):

    #date_creation = forms.DateField(label='Дата создания', initial=datetime.date.today)
    #jt = forms.ModelChoiceField(queryset=JobTitle.objects.all()) #список должностей
    #tjt = forms.ModelChoiceField(queryset=TaskJobTitle.objects.all()) #список чек листов
    date_creation = forms.DateField(label='Дата создания', initial=datetime.date.today, 
    widget=forms.DateInput(attrs={'type': 'date'}))
   
    #jt = forms.ModelChoiceField(queryset=JobTitle.objects.all()) #список должностей
    #tjt = forms.ModelChoiceField(queryset=TaskJobTitle.objects.all()) #список чек листов
    
    class Meta:
        model = TaskExe
        fields = ('date_creation',)

class SelectTasksForm(forms.Form):
    
    #пробую создать форму поля checkbox
    t = 1 
   
class LoginUserForm (AuthenticationForm):
   username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
   password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     username = forms.CharField(label='Логин')
#     password = forms.CharField(label='Пароль')

class ControlTasksForm(forms.Form):

    date_control = forms.DateField(label='Дата заданий', initial=datetime.date.today,widget=forms.DateInput(attrs={'type': 'date'}))
 
    #jt = forms.ModelChoiceField(queryset=JobTitle.objects.all()) #список должностей
    tjt = forms.ModelChoiceField(label='Выбор чек листа', queryset=TaskJobTitle.objects.all(), required=False, widget=forms.Select(attrs={
        'class':'form-select'
    }) ) #список чек листов

class BotForm(forms.Form):

    date_bot = forms.DateField(label='Дата создания', initial=datetime.date.today)
    #jt = forms.ModelChoiceField(queryset=JobTitle.objects.all()) #список должностей
    #tjt = forms.ModelChoiceField(queryset=TaskJobTitle.objects.all()) #список чек листов

class QRPaymentForm(forms.Form):

    QR_sum = forms.CharField(label='Сумма к оплате:', 
    widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100px; font-weight: bold;'}))
    k = 0
    
class AddZakazForm(forms.Form):
    
    # zakaz_date = forms.DateField(label='Дата заявки:', widget=forms.DateInput(attrs={'type': 'date'}))
    
    # zakaz_receiver = forms.ModelChoiceField(label='Объект производства:', queryset=Receiver.objects.all(), required=False, widget=forms.Select(attrs={
    #     'class':'form-select', 'style': 'width: 200px; vertical-align: middle'
    # }) ) #список объектов производства

    k=0        

class AddZakazremarkForm(forms.Form):
    
    # zakaz_date = forms.DateField(label='Дата комментария:', widget=forms.DateInput(attrs={'type': 'date'}))
    # remark = forms.TextInput()
    k = 0

class ExeZakazForm(forms.Form):
    #zakaz_date = forms.DateField(label='Дата заявки:', initial=datetime.date.today(), widget=forms.DateInput(attrs={'type': 'date'}))
    k=0

class AddTabelForm(forms.Form):
    k=0

class EditTabelForm(forms.Form):
    k=0

class AddTabelAdminForm(forms.Form):
    k=0

class TabelReportSimpleForm(forms.Form):
    k=0

class TabelReportForm(forms.Form):
    k=0

class AddStopListForm(forms.Form):
    k=0    
class AddStopListRemarkForm(forms.Form):
    k=0    
class StopListForm(forms.Form): 
    k=0    
class StopListReportForm(forms.Form): 
    k=0    
class AddGraphicForm(forms.Form):
    k=0        
class EditGraphicForm(forms.Form):
    k=0        
class GraphicDayReportSimpleForm(forms.Form):
    k=0        

class AddChListRecForm(forms.Form):
    k = 0

class ChlWorkForm(forms.Form):
    k = 0

class ChlControlForm(forms.Form):
    k = 0

class ChlReportBasicForm(forms.Form):
    k = 0

class TabelReportSimpleFormPan(forms.Form):
    k = 0

class UploadFileForm(forms.Form):
    #file = forms.ImageField
    taskpk = forms.CharField(label="TaskPK")


class ChlControlTaskProblemForm(forms.Form):    
    k = 0

class ChlReportControlForm(forms.Form):
    k = 0

class KPITaskReportForm(forms.Form):
    k = 0
    
class GraphicForm(forms.Form):
    k = 0

class BanketForm(forms.Form):
    k = 0

class AddZakazHimForm(forms.Form):
    k=0        

class AddZakazremarkHimForm(forms.Form):
    k = 0

class ExeZakazHimForm(forms.Form):
    k=0

class NomenHimForm(forms.Form):
    k=0

class DenForm(forms.Form):
    k=0

class DenReportForm (forms.Form):
    k=0

class STaskForm (forms.Form):
    k=0
