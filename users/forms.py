from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('JT', 'OBJ', 'POD', 'TEL', 'TELEGRAMID', 
                                                 'A_Tabel', 'A_TabelAdmin', 'A_TabelReport', 
                                                 'A_TabelReportAdmin', )

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('JT', 'OBJ', 'POD', 'TEL', 'TELEGRAMID', 
                                                 'A_Tabel', 'A_TabelAdmin', 'A_TabelReport', 
                                                 'A_TabelReportAdmin', )

        