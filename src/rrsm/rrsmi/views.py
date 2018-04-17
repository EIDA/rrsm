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
from .models import Link, SearchEvent
from .forms import SearchEventsForm


class HomeListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'events.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data, ws_url = FdsnEventManager().get_events(days_back=31)
        context['breadcrumb'] = 'Home'
        context['events'] = data.events
        context['ws_url'] = ws_url
        return context


class RecentEventsListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'events.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data, ws_url = FdsnEventManager().get_events(
            days_back=int(self.kwargs.get('days'))
            )
        context['breadcrumb'] = 'Recent events'
        context['events'] = data.events
        context['ws_url'] = ws_url
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
        context['motion_data'], context['ws_url'] = \
            FdsnMotionManager().get_event_details(
                self.kwargs.get('event_public_id')
                )
        return context


class LinksListView(ListView):
    model = Link
    context_object_name = 'links'
    template_name = 'links.html'

    def get_queryset(self):
        queryset = Link.objects.order_by('category')
        return queryset


def search_events(request):
    if request.method == 'POST':
        search_form = SearchEventsForm(request.POST)
        if search_form.is_valid():
            data, ws_url = FdsnEventManager().get_events(
                event_id=search_form.cleaned_data['event_id'],
                date_start=search_form.cleaned_data['date_start'],
                date_end=search_form.cleaned_data['date_end'],
                magnitude_min=search_form.cleaned_data['magnitude_min'],
                network_code=search_form.cleaned_data['network_code'],
                station_code=search_form.cleaned_data['station_code'],
                level=search_form.cleaned_data['level']
            )

            if data:
                queryset = data.events
            else:
                queryset = None

            return render(
                request,
                'events.html',
                {
                    'events': queryset,
                    'breadcrumb': 'Search result',
                    'ws_url': ws_url
                }
            )
        else:
            return render(
                request,
                'search_events.html',
                {
                    'form': search_form
                }
            )
    else:
        search_form = SearchEventsForm(instance=SearchEvent())
        return render(
            request,
            'search_events.html',
            {
                'form': search_form
            }
        )


def custom_404(request, exception=None):
    '''HTTP 404 custom handler
    '''
    return render_to_response('404.html', {'exception': exception})


def custom_500(request, exception=None):
    '''HTTP 500 custom handler
    '''
    return render_to_response('500.html', {'exception': exception})
