# Generated by Django 4.2.20 on 2025-04-18 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_kpimetric_kpi'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='name',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Описание'),
        ),
    ]
