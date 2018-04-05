# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum

from django.db import models, transaction
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from markdown import markdown


STRING_LENGTH_SHORT = 256
STRING_LENGTH_MEDIUM = 1024
STRING_LENGTH_LONG = 16384


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    about = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    location = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    agency = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    department = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    telephone = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    skype = models.CharField(max_length=STRING_LENGTH_MEDIUM, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Profile of: {0}'.format(self.user)


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
