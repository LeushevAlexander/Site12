# Generated by Django 4.1.3 on 2022-12-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20221129_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskexe',
            name='time_exe',
            field=models.DateTimeField(null=True, verbose_name='Дата/время исполнения'),
        ),
    ]
