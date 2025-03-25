from django.db.models import Count

from .models import *


menu = [
 #       {'title': "Список должностей", 'url_name': 'JobTitleList'},
 #       {'title': "Список  чек-листов", 'url_name': 'TaskJobTitleList'},
 #       {'title': "Список  заданий", 'url_name': 'TaskList'},
 #       {'title': "Создание заданий", 'url_name': 'AddTasks'},
 #       {'title': "Просмотр заданий", 'url_name': 'SelectTasks'},
 #       {'title': "Контроль заданий", 'url_name': 'ControlTasks'},
        {'title': "О нас...", 'url_name': 'About'},
]
# def getmenu(request):

#     # определяю меню исходя из пользователя (полномочий, администратор или нет)
#     jt=request.user.JT
#     if jt.id==1:
#         menu = [
#         {'title': "Список должностей", 'url_name': 'JobTitleList'},
#         {'title': "Список  чек-листов", 'url_name': 'TaskJobTitleList'},
#         {'title': "Список  заданий", 'url_name': 'TaskList'},
#         {'title': "Создание заданий", 'url_name': 'AddTasks'},
#         {'title': "Выполнение заданий", 'url_name': 'SelectTasks'},
#         {'title': "Контроль заданий", 'url_name': 'ControlTasks'},
#         {'title': "О нас...", 'url_name': 'About'},
#         ]
#     else:
#        menu = [
#         {'title': "Выполнение", 'url_name': 'SelectTasks'},
#         {'title': "О нас...", 'url_name': 'About'},  
#        ]      

#     return menu      

class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        
        #mn = getmenu(self.request)
        
        context = kwargs
        #cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            #user_menu.pop(1)
            user_menu=menu

        context['menu'] = user_menu

        #context['cats'] = cats
        #if 'cat_selected' not in context:
        #    context['cat_selected'] = 0
        
        return context
