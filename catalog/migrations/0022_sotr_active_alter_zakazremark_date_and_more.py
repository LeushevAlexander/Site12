# Generated by Django 4.1.3 on 2023-02-20 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_den_podrazd_sotr_vidmer_vidnach_alter_payment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sotr',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='zakazremark',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='zakazremark',
            name='remark',
            field=models.CharField(max_length=200, verbose_name='Комментарий'),
        ),
    ]
