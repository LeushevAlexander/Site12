# Generated by Django 4.2.13 on 2025-01-10 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_vidopl_remove_banket_avtor_remove_banket_sbor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiver',
            name='img',
            field=models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='static/IMG', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='stoplist',
            name='ost',
            field=models.IntegerField(default=0, null=True, verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='stoplist',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autor', to='catalog.sotr', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='stoplist',
            name='autor_exe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autor_exe', to='catalog.sotr', verbose_name='Исключил автор'),
        ),
        migrations.CreateModel(
            name='StopListRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecreated', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
                ('remark', models.CharField(max_length=50, null=True, verbose_name='Комментарий')),
                ('causeinfo', models.CharField(max_length=150, null=True, verbose_name='Информация')),
                ('date_exe', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата/время исключения')),
                ('ost', models.IntegerField(default=0, null=True, verbose_name='Остаток')),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autor1', to='catalog.sotr', verbose_name='Автор')),
                ('autor_exe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='autor_exe1', to='catalog.sotr', verbose_name='Исключил автор')),
                ('cause', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.causelist', verbose_name='Причина')),
                ('obj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.receiver', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Стоп лист комментарий',
                'verbose_name_plural': 'Стоп лист комментарий',
            },
        ),
    ]
