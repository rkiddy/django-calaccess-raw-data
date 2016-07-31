#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for tracking CAL-ACCESS updates over time.
"""
from __future__ import unicode_literals
from django.db import models
from hurry.filesize import size as sizeformat
from calaccess_raw import archive_directory_path, get_model_list
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RawDataVersion(models.Model):
    """
    A version of CAL-ACCESS raw source data, typically released every day.
    """
    release_datetime = models.DateTimeField(
        unique=True,
        null=False,
        verbose_name='date and time of release',
        help_text='Date and time the version of the CAL-ACCESS database was released '
                  '(value of last-modified field in HTTP response header)'
    )
    size = models.BigIntegerField(
        null=False,
        verbose_name='size of raw data version in bytes',
        help_text='Size of the .ZIP file for this version of the CAL-ACCESS raw source data '
                  '(value of content-length field in HTTP response header)'
    )
    update_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time update started',
        help_text='Date and time when the update to the CAL-ACCESS version started',
    )
    update_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time update finished',
        help_text='Date and time when the update to the CAL-ACCESS version finished',
    )
    download_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time download started',
        help_text='Date and time when the download of the CAL-ACCESS database export started',
    )
    download_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time download finished',
        help_text='Date and time when the download of the CAL-ACCESS database export finished',
    )
    extract_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time extraction started',
        help_text='Date and time when extraction of the CAL-ACCESS data files started',
    )
    extract_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time extraction finished',
        help_text='Date and time when extraction of the CAL-ACCESS data files finished',
    )
    download_zip_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='download files zip file',
        help_text='An archive of the original zipped file downloaded from '
                     'CAL-ACCESS.'
    )
    clean_zip_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='cleaned files zip archive',
        help_text='An archive zip of cleaned (and error log) files'
    )

    class Meta:
        app_label = 'calaccess_raw'
        verbose_name = 'CAL-ACCESS raw data version'
        ordering = ('-release_datetime',)

    def __str__(self):
        return str(self.release_datetime)

    @property
    def update_completed(self):
        """
        Check if the database update to the version completed.

        Return True or False.
        """
        if self.update_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def update_stalled(self):
        """
        Check if the database update to the version started but did not complete.

        Return True or False.
        """
        if self.update_start_datetime and not self.update_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled

    @property
    def download_completed(self):
        """
        Check if the download of the version's zip file completed.

        Return True or False.
        """
        if self.download_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def download_stalled(self):
        """
        Check if the download of the version's zip file started but did not complete.
        """
        if self.download_start_datetime and not self.download_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled

    @property
    def extract_completed(self):
        """
        Return True if the extraction of the version's raw data files completed.
        """
        if self.extract_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def extract_stalled(self):
        """
        Check if the download of the version's zip file started but did not complete.
        """
        if self.extract_start_datetime and not self.extract_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled

    def pretty_size(self):
        """
        Returns a prettified version of the file size.
        """
        if not self.size:
            return None
        return sizeformat(self.size)
    pretty_size.short_description = 'size'
    pretty_size.admin_order_field = 'size'


@python_2_unicode_compatible
class RawDataFile(models.Model):
    """
    A data file included in a version of the CAL-ACCESS raw source data.
    """
    version = models.ForeignKey(
        'RawDataVersion',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='raw data version',
        help_text='Foreign key referencing the version of the raw '
                  'source data in which the file was included'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='raw data file name',
        help_text='Name of the raw source data file without extension',
    )
    download_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='download records count',
        help_text='Count of records in the original file downloaded from CAL-ACCESS'
    )
    clean_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='clean records count',
        help_text='Count of records in the cleaned file generated by calaccess_raw'
    )
    load_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='load records count',
        help_text="Count of records in the loaded from cleaned file into "
                  "calaccess_raw's data model"
    )
    download_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='download columns count',
        help_text='Count of columns in the original file downloaded from CAL-ACCESS'
    )
    clean_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='clean columns count',
        help_text='Count of columns in the cleaned file generated by calaccess_raw'
    )
    load_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='load columns count',
        help_text='Count of columns on the loaded calaccess_raw data model'
    )
    download_file_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='archive of download file',
        help_text='An archive of the original raw data file downloaded '
                     'from CAL-ACCESS.'
    )
    download_file_size = models.BigIntegerField(
        null=False,
        default=0,
        verbose_name='size of raw data file in bytes',
        help_text='Size of the .TSV file'
    )
    clean_file_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='archive of clean file',
        help_text='An archive of the raw data file after being cleaned.'
    )
    clean_file_size = models.BigIntegerField(
        null=False,
        default=0,
        verbose_name='size of clean data file in bytes',
        help_text='Size of the .CSV file'
    )
    error_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='error count',
        help_text='Count of records in the original download that could not '
                  'be parsed and are excluded from the cleaned file.'
    )
    error_log_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='archive of error log',
        help_text='An archive of the error log containing lines from the '
                  'original download file that could not be parsed and are '
                  'excluded from the cleaned file.'
    )
    clean_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time cleaning started',
        help_text='Date and time when the cleaning of the file started',
    )
    clean_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time cleaning finished',
        help_text='Date and time when the cleaning of the file finished',
    )
    load_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time loading started',
        help_text='Date and time when the loading of the file started',
    )
    load_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time extraction finished',
        help_text='Date and time when the loading of the file finished',
    )

    class Meta:
        app_label = 'calaccess_raw'
        unique_together = (('version', 'file_name'),)
        verbose_name = 'CAL-ACCESS raw data file'
        ordering = ('-version_id', 'file_name',)

    def __str__(self):
        return self.file_name

    def pretty_download_file_size(self):
        """
        Returns a prettified version of the download_file_size size.
        """
        if not self.download_file_size:
            return None
        return sizeformat(self.download_file_size)
    pretty_download_file_size.short_description = 'download file size'
    pretty_download_file_size.admin_order_field = 'download file size'

    def pretty_clean_file_size(self):
        """
        Returns a prettified version of the clean_file_size size.
        """
        if not self.clean_file_size:
            return None
        return sizeformat(self.clean_file_size)
    pretty_clean_file_size.short_description = 'clean file size'
    pretty_clean_file_size.admin_order_field = 'clean file size'

    @property
    def model(self):
        """
        Returns the RawDataFile's corresponding CalAccess database model object.
        """
        return [
            m for m in get_model_list() if m().db_table == self.file_name
        ][0]


@python_2_unicode_compatible
class RawDataCommand(models.Model):
    """
    A call of a command from this application with start and finish times.
    """
    version = models.ForeignKey(
        'RawDataVersion',
        on_delete=models.CASCADE,
        related_name='command_logs',
        verbose_name='raw data version',
        help_text='Foreign key referencing the version of the raw '
                  'source data on which the command was performed'
    )
    command = models.CharField(
        max_length=50,
        verbose_name='command name',
        help_text='Name of the command performed on the given version of the raw source data'
    )
    called_by = models.ForeignKey(
        'self',
        related_name="called",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='called by',
        help_text='Foreign key refencing log of the CalAccessCommand that '
                  'called this command. Null represents call from command line'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='raw data file name',
        help_text='Name of the raw source data file without extension',
    )
    start_datetime = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='date and time command started',
        help_text='Date and time when the given command started on the '
                  'given version of the raw source data'
    )
    finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time command finished',
        help_text='Date and time when the given command finished on '
                  'the given version of the raw source data'
    )

    class Meta:
        app_label = 'calaccess_raw'
        verbose_name = 'CAL-ACCESS raw data command'
        ordering = ('-id',)

    def __str__(self):
        return self.command
