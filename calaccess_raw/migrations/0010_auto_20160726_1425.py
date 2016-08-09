# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 14:25
from __future__ import unicode_literals

import calaccess_raw
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_raw', '0009_rawdataversion_clean_zip_archive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rawdataversion',
            options={'get_latest_by': 'release_datetime', 'ordering': ('-release_datetime',), 'verbose_name': 'CAL-ACCESS raw data version'},
        ),
        migrations.RemoveField(
            model_name='rawdataversion',
            name='zip_file_archive',
        ),
        migrations.AddField(
            model_name='rawdataversion',
            name='download_zip_archive',
            field=models.FileField(blank=True, help_text='An archive of the original zipped file downloaded from CAL-ACCESS.', max_length=255, upload_to=calaccess_raw.archive_directory_path, verbose_name='download files zip file'),
        ),
    ]