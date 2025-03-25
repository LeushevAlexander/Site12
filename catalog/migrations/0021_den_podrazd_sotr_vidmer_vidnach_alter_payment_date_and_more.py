# Generated by Django 4.1.4 on 2023-02-17 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_ei_nomen_payment_receiver_review_source_zakazremark_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Den',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('vnal', models.FloatField(default=0, null=True, verbose_name='Выручка Нал.')),
                ('vbnal', models.FloatField(default=0, null=True, verbose_name='Выручка Б/Нал.')),
                ('vbc', models.FloatField(default=0, null=True, verbose_name='Выручка БС.')),
                ('vpp', models.FloatField(default=0, null=True, verbose_name='Выручка П/П')),
                ('vpr', models.FloatField(default=0, null=True, verbose_name='Выручка Предс.')),
                ('vb', models.FloatField(default=0, null=True, verbose_name='Выручка Бар')),
                ('vk', models.FloatField(default=0, null=True, verbose_name='Выручка Кух.')),
                ('chn', models.FloatField(default=0, null=True, verbose_name='Чай/Нал.')),
                ('chbn', models.FloatField(default=0, null=True, verbose_name='Чай/БНал.')),
                ('kolg', models.FloatField(default=0, null=True, verbose_name='Кол.гостей')),
                ('avtor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('datecreated', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'Рабочий день',
                'verbose_name_plural': 'Рабочие дни',
            },
        ),
        migrations.CreateModel(
            name='Podrazd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, null=True, verbose_name='Подразделение')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
        migrations.CreateModel(
            name='Sotr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, null=True, verbose_name='Сотрудник')),
                ('stavka', models.IntegerField(default=0, null=True, verbose_name='Ставка')),
                ('div', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.podrazd', verbose_name='Подразделение')),
                ('ei', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.ei', verbose_name='Ед.')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Vidmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, null=True, verbose_name='Вид мероприятия')),
            ],
            options={
                'verbose_name': 'Вид мероприятия',
                'verbose_name_plural': 'Виды мероприятий',
            },
        ),
        migrations.CreateModel(
            name='Vidnach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, null=True, verbose_name='Вид начисления')),
            ],
            options={
                'verbose_name': 'Вид начисления',
                'verbose_name_plural': 'Виды начисления',
            },
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Дата/Время'),
        ),
        migrations.CreateModel(
            name='Vipl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('sum', models.FloatField(default=0, null=True, verbose_name='Сумма')),
                ('avtor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('datecreated', models.DateTimeField(null=True)),
                ('sotr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.sotr', verbose_name='Сотрудник')),
                ('vidnach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.vidnach', verbose_name='Вид начисл.')),
            ],
            options={
                'verbose_name': 'Выплата',
                'verbose_name_plural': 'Выплаты',
            },
        ),
        migrations.CreateModel(
            name='Tabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('kol', models.FloatField(default=0, null=True, verbose_name='Количество')),
                ('sum', models.FloatField(default=0, null=True, verbose_name='Сумма')),
                ('stavka', models.FloatField(default=0, null=True, verbose_name='Ставка')),
                ('avtor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('datecreated', models.DateTimeField(null=True)),
                ('div', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.podrazd', verbose_name='Подразделение')),
                ('ei', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.ei', verbose_name='Е.И.')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
                ('sotr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.sotr', verbose_name='Сотрудник')),
                ('vidnach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.vidnach', verbose_name='Вид начисл.')),
            ],
            options={
                'verbose_name': 'Табель',
                'verbose_name_plural': 'Табели',
            },
        ),
        migrations.CreateModel(
            name='Banket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('sum', models.FloatField(default=0, null=True, verbose_name='Сумма')),
                ('sbor', models.FloatField(default=0, null=True, verbose_name='Сбор')),
                ('kolg', models.FloatField(default=0, null=True, verbose_name='Кол.гостей')),
                ('remark', models.TextField(max_length=300, null=True, verbose_name='Комментарий')),
                ('avtor', models.CharField(max_length=30, null=True, verbose_name='Автор')),
                ('datecreated', models.DateTimeField(null=True)),
                ('vidmer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.vidmer', verbose_name='Вид меропр.')),
            ],
            options={
                'verbose_name': 'Банкет',
                'verbose_name_plural': 'Банкеты',
            },
        ),
    ]
