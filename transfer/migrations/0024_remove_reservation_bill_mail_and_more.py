# Generated by Django 4.2.1 on 2023-09-07 11:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0023_reservation_bill_mail_reservation_mail_context_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='bill_mail',
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment_method',
            field=models.CharField(choices=[('Araçta Nakit', 'Araçta Nakit'), ('EFT/Havale', 'EFT/Havale')], default='Araçta Nakit', max_length=20, verbose_name='Ödeme Yöntemi'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 7), verbose_name='Transfer Tarihi'),
        ),
    ]