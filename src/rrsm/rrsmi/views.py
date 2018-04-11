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

from .forms import \
    UserForm, ProfileForm

from .fdsn.fdsn_manager import FdsnEventManager


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
            queryset = FdsnEventManager().get_recent_events(int(self.kwargs.get('days'))).events
        except:
            raise
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = 'Recent events'
        return context


class UserDetailsListView(ListView):
    model = User
    context_object_name = 'user_data'
    template_name = 'user_details.html'

    def get_queryset(self):
        try:
            queryset = User.objects.\
                get(username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("User does not exist!")
        return queryset


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('my_account')
        else:
            return render(request, 'my_account.html', {
                'user_form': user_form, 'profile_form': profile_form
                })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'my_account.html', {
            'user_profile': request.user.profile,
            'user_form': user_form,
            'profile_form': profile_form
            })


def custom_404(request, exception=None):
    '''HTTP 404 custom handler
    '''
    return render_to_response('404.html', {'exception': exception})


def custom_500(request, exception=None):
    '''HTTP 500 custom handler
    '''
    return render_to_response('500.html', {'exception': exception})
