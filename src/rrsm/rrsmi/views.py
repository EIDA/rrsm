# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
from functools import reduce

from django.http import Http404
from django.shortcuts import \
    get_object_or_404, redirect, render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.db.models import Q, Count

from .fdsn.fdsn_manager import FdsnEventManager, FdsnMotionManager


class HomeListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'recent_events.html'

    def get_queryset(self):
        try:
            queryset = FdsnEventManager().get_recent_events(31).events
        except:
            raise
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = 'Home'
        return context


class RecentEventsListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'recent_events.html'

    def get_queryset(self):
        try:
            queryset = FdsnEventManager().get_recent_events(
                int(self.kwargs.get('days'))
            ).events
        except:
            raise
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = 'Recent events'
        return context


class EventDetailsListView(ListView):
    model = None
    context_object_name = None
    template_name = 'event_details.html'

    def get_queryset(self):
        try:
            queryset = None
        except:
            raise
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['motion_data'], context['odc_ws_link'] = \
            FdsnMotionManager().get_event_details(
                self.kwargs.get('event_public_id')
                )
        return context


def custom_404(request, exception=None):
    '''HTTP 404 custom handler
    '''
    return render_to_response('404.html', {'exception': exception})


def custom_500(request, exception=None):
    '''HTTP 500 custom handler
    '''
    return render_to_response('500.html', {'exception': exception})
