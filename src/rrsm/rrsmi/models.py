# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models

STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384
COORD_INTEGERS = 3
COORD_DECIMALS = 5
PGA_PGV_INTEGERS = 5
PGA_PGV_DECIMALS = 5
MAG_INTEGERS = 2
MAG_DECIMALS = 1


class SearchEvent(models.Model):
    event_id = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    date_start = models.DateField(default='', blank=True)
    date_end = models.DateField(default='', blank=True)
    magnitude_min = models.DecimalField(
        max_digits=MAG_INTEGERS + MAG_DECIMALS,
        decimal_places=MAG_DECIMALS,
        blank=True
    )
    network_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    station_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    event_lat_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lat_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lon_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lon_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )

    class Meta:
        managed = False


class SearchPeakMotions(models.Model):
    pga_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pga_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )

    class Meta:
        managed = False


class SearchCombined(models.Model):
    magnitude_min = models.DecimalField(
        max_digits=MAG_INTEGERS + MAG_DECIMALS,
        decimal_places=MAG_DECIMALS,
        blank=True
    )
    pga_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pga_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    stat_lat_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lat_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lon_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lon_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )

    class Meta:
        managed = False


class SearchCustom(models.Model):
    event_id = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    date_start = models.DateField(default='', blank=True)
    date_end = models.DateField(default='', blank=True)
    magnitude_min = models.DecimalField(
        max_digits=MAG_INTEGERS + MAG_DECIMALS,
        decimal_places=MAG_DECIMALS,
        blank=True
    )
    network_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    station_code = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )
    pga_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pga_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_min = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    pgv_max = models.DecimalField(
        max_digits=PGA_PGV_INTEGERS + PGA_PGV_DECIMALS,
        decimal_places=PGA_PGV_DECIMALS,
        blank=True
    )
    stat_lat_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lat_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lon_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    stat_lon_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lat_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lat_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lon_min = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )
    event_lon_max = models.DecimalField(
        max_digits=COORD_INTEGERS + COORD_DECIMALS,
        decimal_places=COORD_DECIMALS,
        blank=True
    )

    class Meta:
        managed = False
