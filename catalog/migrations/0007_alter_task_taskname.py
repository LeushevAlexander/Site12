# Generated by Django 4.1.3 on 2022-11-18 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_taskjobtitle_tasks_alter_taskjobtitle_jobtitle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='taskname',
            field=models.CharField(max_length=150, verbose_name='Название задачи'),
        ),
    ]
