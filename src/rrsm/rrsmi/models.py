# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class SearchEvent(models.Model):
    event_id = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    date_start = models.DateField(default='', blank=True)
    date_end = models.DateField(default='', blank=True)
    magnitude_min = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True
    )
    network_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    station_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    event_lat_min = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    event_lat_max = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    event_lon_min = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    event_lon_max = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )

    class Meta:
        managed = False


class SearchPeakMotions(models.Model):
    pga_min = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pga_max = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pgv_min = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pgv_max = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )

    class Meta:
        managed = False


class SearchCombined(models.Model):
    magnitude_min = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True
    )
    pga_min = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pga_max = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pgv_min = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    pgv_max = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True
    )
    stat_lat_min = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    stat_lat_max = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    stat_lon_min = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )
    stat_lon_max = models.DecimalField(
        max_digits=8, decimal_places=5, blank=True
    )

    class Meta:
        managed = False
