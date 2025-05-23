# Generated by Django 4.2.13 on 2024-12-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_a_graphic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='A_Banket',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Просмотр раздела банкеты'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='A_BanketEdit',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Созд/Изм/Удал. банкетов'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='A_BanketFin',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Просмотр фин.инф. банкетов'),
        ),
    ]
