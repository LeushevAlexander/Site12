from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    lisl_display = ('username', 'JT', 'OBJ', 'POD', 'sotr', 'TEL', 'TELEGRAMID', 
                    'A_Tabel', 'A_TabelAdmin', 'A_TabelReport', 'A_TabelReportAdmin', 
                    'A_Den', 'A_DenReport', 'A_Graphic', 'A_Banket', 'A_BanketFin', 'A_BanketEdit')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Реквизиты пользователя:', {'fields': ('JT', 'OBJ', 'POD', 'sotr', 'TEL', 'TELEGRAMID', 'A_Tabel', 
        'A_TabelAdmin', 'A_TabelReport', 'A_TabelReportAdmin', 'A_Den', 'A_DenReport', 'A_Graphic', 'A_Banket', 'A_BanketFin', 'A_BanketEdit')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Реквизиты пользователя:', {'fields': ('JT', 'OBJ', 'sotr', 'POD', 'TEL', 'TELEGRAMID', 'A_Tabel', 'A_TabelAdmin', 
        'A_TabelReport', 'A_TabelReportAdmin',  'A_Den', 'A_DenReport', 'A_Graphic', 'A_Banket', 'A_BanketFin', 'A_BanketEdit')}),
    )

   #fieldsets = UserAdmin.fieldsets + (
   #     ('Дополнительно: ', {'fields': ('jobtitle', )})
   # )

   # add_fieldsets = UserAdmin.add_fieldsets + (
   #     ('Дополнительно: ', {'fields': ('jobtitle', )})
   # )

admin.site.register(CustomUser, CustomUserAdmin)    

