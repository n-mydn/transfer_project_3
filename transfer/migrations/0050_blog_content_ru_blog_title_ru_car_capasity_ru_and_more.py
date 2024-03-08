# Generated by Django 4.2.1 on 2023-12-17 12:14

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0049_webabout_alter_reservation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='İçerik'),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Başlık'),
        ),
        migrations.AddField(
            model_name='car',
            name='capasity_ru',
            field=models.CharField(max_length=20, null=True, verbose_name='Kapasite'),
        ),
        migrations.AddField(
            model_name='car',
            name='fromwhere_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='transfer.fromwhere', verbose_name='Nereden'),
        ),
        migrations.AddField(
            model_name='car',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='car',
            name='towhere_ru',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='transfer.towhere', verbose_name='Nereye'),
        ),
        migrations.AddField(
            model_name='extras',
            name='name_ru',
            field=models.CharField(max_length=20, null=True, verbose_name='Ad'),
        ),
        migrations.AddField(
            model_name='extras',
            name='price_ru',
            field=models.IntegerField(null=True, verbose_name='Ücret'),
        ),
        migrations.AddField(
            model_name='fromwhere',
            name='name_ru',
            field=models.CharField(max_length=300, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='homepagearticleone',
            name='content_ru',
            field=models.TextField(null=True, verbose_name='İçerik'),
        ),
        migrations.AddField(
            model_name='homepagearticleone',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Başlık'),
        ),
        migrations.AddField(
            model_name='homepagearticletwo',
            name='content_ru',
            field=models.TextField(null=True, verbose_name='İçerik'),
        ),
        migrations.AddField(
            model_name='homepagearticletwo',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Başlık'),
        ),
        migrations.AddField(
            model_name='towhere',
            name='name_ru',
            field=models.CharField(max_length=300, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='transfer',
            name='fromwhere_ru',
            field=models.ForeignKey(help_text='Lütfen listeden bir öge seçin.', null=True, on_delete=django.db.models.deletion.CASCADE, to='transfer.fromwhere', verbose_name='Nereden'),
        ),
        migrations.AddField(
            model_name='transfer',
            name='towhere_ru',
            field=models.ForeignKey(help_text='Lütfen listeden bir öge seçin.', null=True, on_delete=django.db.models.deletion.CASCADE, to='transfer.towhere', verbose_name='Nereye'),
        ),
        migrations.AddField(
            model_name='transfertypes',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='İçerik'),
        ),
        migrations.AddField(
            model_name='transfertypes',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Başlık'),
        ),
        migrations.AddField(
            model_name='webabout',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='İçerik'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='time_of_return',
            field=models.TimeField(default='15:14', verbose_name='Dönüş Saati'),
        ),
    ]