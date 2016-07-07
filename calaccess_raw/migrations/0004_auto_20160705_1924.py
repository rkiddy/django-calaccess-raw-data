# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-05 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_raw', '0003_auto_20160705_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdatafile',
            name='clean_file_size',
            field=models.IntegerField(default=0, help_text='Size of the .CSV file', verbose_name='size of clean data file in bytes'),
        ),
        migrations.AlterField(
            model_name='rawdatafile',
            name='download_file_size',
            field=models.IntegerField(default=0, help_text='Size of the .TSV file', verbose_name='size of raw data file in bytes'),
        ),
    ]