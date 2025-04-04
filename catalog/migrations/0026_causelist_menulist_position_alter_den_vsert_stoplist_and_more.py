# Generated by Django 4.1.4 on 2024-05-21 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_tabel_t1_tabel_t2'),
    ]

    operations = [
        migrations.CreateModel(
            name='CauseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Причина')),
            ],
            options={
                'verbose_name': 'Причина',
                'verbose_name_plural': 'Причины',
            },
        ),
        migrations.CreateModel(
            name='MenuList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Блюдо')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, verbose_name='Название должности')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
            },
        ),
        migrations.AlterField(
            model_name='den',
            name='vsert',
            field=models.FloatField(default=0, null=True, verbose_name='Выручка Сертификат.'),
        ),
        migrations.CreateModel(
            name='StopList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecreated', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
                ('autor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('causeinfo', models.CharField(max_length=150, null=True, verbose_name='Информация')),
                ('autor_exe', models.CharField(default='', max_length=30, null=True, verbose_name='Исключил')),
                ('date_exe', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата/время исключения')),
                ('cause', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.causelist', verbose_name='Причина')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.menulist', verbose_name='Блюдо')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Стоп лист',
                'verbose_name_plural': 'Стоп лист',
            },
        ),
        migrations.CreateModel(
            name='Graphic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('t1', models.CharField(blank=True, max_length=10, null=True, verbose_name='t Приход')),
                ('t2', models.CharField(blank=True, max_length=10, null=True, verbose_name='t Уход')),
                ('kol', models.FloatField(default=0, null=True, verbose_name='Количество')),
                ('sum', models.FloatField(default=0, null=True, verbose_name='Сумма')),
                ('autor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('datecreated', models.DateTimeField(null=True)),
                ('ch_autor', models.CharField(max_length=30, null=True, verbose_name='Автор изм.')),
                ('datechanged', models.DateTimeField(null=True)),
                ('div', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.podrazd', verbose_name='Подразделение')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
                ('pos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.position', verbose_name='Позиция')),
                ('sotr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.sotr', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'График сотрудников',
                'verbose_name_plural': 'График сотрудников',
            },
        ),
    ]
