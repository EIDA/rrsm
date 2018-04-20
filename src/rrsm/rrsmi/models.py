# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models, transaction
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth.models import User


STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class FdsnNode(models.Model):
    code = models.CharField(
        primary_key=True, max_length=STRING_LENGTH_SHORT, unique=True)
    description = models.CharField(
        max_length=STRING_LENGTH_SHORT, default='', blank=True)
    url_event = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_motion = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_shakemap = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)
    url_waveform = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, default='', blank=True)

    def __str__(self):
        return self.code


class Link(models.Model):
    url = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, null=True, blank=True
    )
    category = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, null=True, blank=True
    )
    description = models.CharField(
        max_length=STRING_LENGTH_MEDIUM, null=True, blank=True
    )

    def __str__(self):
        return '{0} - {1}'.format(
            self.url,
            self.description
        )


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
    level = models.CharField(
        max_length=STRING_LENGTH_SHORT, blank=True
    )

    class Meta:
        managed = False
