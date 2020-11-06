# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
import json
from collections import defaultdict, OrderedDict
from datetime import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import \
get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.db.models import Q, Count

from .base_classes import RrsmHelpers

from .fdsn.fdsn_manager import \
    FdsnMotionManager, FdsnShakemapManager, \
    FdsnWaveformManager, FdsnDataselectManager

from .models import \
    SearchEvent, SearchPeakMotions, \
    SearchCombined, SearchCustom
from .forms import \
    SearchEventsForm, SearchPeakMotionsForm, \
    SearchCombinedForm, SearchCustomForm

from .logger import RrsmLoggerMixin


class HomeListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'events.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        motion_data, ws_url = FdsnMotionManager().get_simple_event_list(days_back=31)
        context['breadcrumb'] = 'Home (events from last 31 days)'
        context['motion_data'] = motion_data
        context['ws_url'] = ws_url
        context['is_homepage'] = True
        return context


class AboutListView(ListView):
    model = None
    template_name = 'about.html'

    def get_queryset(self):
        return None


class RecentEventsListView(ListView):
    model = None
    context_object_name = 'events'
    template_name = 'events.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        motion_data, ws_url = FdsnMotionManager().get_simple_event_list(
            days_back=int(self.kwargs.get('days'))
        )
        context['breadcrumb'] = 'Recent events'
        context['motion_data'] = motion_data
        context['ws_url'] = ws_url
        context['is_homepage'] = True
        return context


class EventDetailsListView(ListView, RrsmLoggerMixin):
    model = None
    context_object_name = None
    template_name = 'event_details.html'

    def __init__(self):
        RrsmLoggerMixin.__init__(self)

    def get_queryset(self):
        try:
            queryset = None
        except Exception as e:
            raise e
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_public_id')
        fdsn_motion_man = FdsnMotionManager()
        fdsn_shakemap_man = FdsnShakemapManager()
        fdsn_waveform_man = FdsnWaveformManager()

        motion_data, ws_url = fdsn_motion_man.get_event_details(event_id)
        chart_pga, chart_pgv = self.get_sensor_channels_charts(motion_data)
        shakemap_url = fdsn_shakemap_man.get_shakemap_url(event_id)
        waveform_url = fdsn_waveform_man.get_waveform_url(event_id)

        context['motion_data'] = motion_data
        context['ws_url'] = ws_url
        context['chart_pga'] = chart_pga
        context['chart_pgv'] = chart_pgv
        context['shakemap_url'] = shakemap_url
        context['waveform_url'] = waveform_url
        return context

    def get_sensor_channels_charts(self, motion_data):
        try:
            if not motion_data:
                return None, None

            data_pga = list()
            data_pgv = list()

            for s in motion_data.stations:
                for sc in s.sensor_channels:
                    data_pga.append({
                        'name': f'{s.network_code}.{s.station_code}.{sc.channel_code}',
                        'x': s.epicentral_distance,
                        'y': sc.pga_value * 100,
                        'channel': sc.channel_code
                    })
                    data_pgv.append({
                        'name': f'{s.network_code}.{s.station_code}.{sc.channel_code}',
                        'x': s.epicentral_distance,
                        'y': sc.pgv_value * 100,
                        'channel': sc.channel_code
                    })

            chart_pga = {
                'exporting': {
                    'chartOptions': {
                        'plotOptions': {
                            'series': {
                                'dataLabels': {
                                    'enabled': 'true'
                                }
                            }
                        }
                    },
                    'fallbackToExportServer': 'false'
                },
                'tooltip': {
                    'pointFormat': '<b>{point.name}</b><br><b>Epicentral distance [km]:</b> {point.x}<br><b>PGA [cm/s^2]:</b> {point.y}'
                },
                'chart': {'type': 'scatter'},
                'title': {'text': 'PGA vs Epicentral distance'},
                'xAxis': {
                    'title': {
                        'text': 'Epicentral distance [km]'
                    },
                    'type': 'logarithmic',
                },
                'yAxis': {
                    'title': {
                        'text': 'PGA [cm/s^2]'
                    },
                    'type': 'logarithmic'
                },
                'series': []
            }

            chart_pgv = {
                'exporting': {
                    'chartOptions': {
                        'plotOptions': {
                            'series': {
                                'dataLabels': {
                                    'enabled': 'true'
                                }
                            }
                        }
                    },
                    'fallbackToExportServer': 'false'
                },
                'tooltip': {
                    'pointFormat': '<b>{point.name}</b><br><b>Epicentral distance [km]:</b> {point.x}<br><b>PGV [cm/s]:</b> {point.y}'
                },
                'chart': {'type': 'scatter'},
                'title': {'text': 'PGV vs Epicentral distance'},
                'xAxis': {
                    'title': {
                        'text': 'Epicentral distance [km]'
                    },
                    'type': 'logarithmic'
                },
                'yAxis': {
                    'title': {
                        'text': 'PGV [cm/s]'
                    },
                    'type': 'logarithmic'
                },
                'series': []
            }

            channels_pga = {c['channel'] for c in data_pga}
            channels_pgv = {c['channel'] for c in data_pgv}

            for c in channels_pga:
                chart_pga['series'].append({
                    'name': c,
                    'data': [x for x in data_pga if x['channel'] == c]
                })

            for c in channels_pgv:
                chart_pgv['series'].append({
                    'name': c,
                    'data': [x for x in data_pgv if x['channel'] == c]
                })

            dump_pga = json.dumps(chart_pga)
            dump_pgv = json.dumps(chart_pgv)
            return dump_pga, dump_pgv
        except Exception as e:
            self.log_exception(e)
            return None, None


class StationStreamsListView(ListView, RrsmLoggerMixin):
    model = None
    context_object_name = None
    template_name = 'station_streams.html'

    def __init__(self):
        RrsmLoggerMixin.__init__(self)

    def get_queryset(self):
        try:
            queryset = None
        except Exception as e:
            raise e
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_public_id')
        network_code = self.kwargs.get('network_code')
        station_code = self.kwargs.get('station_code')
        fdsn_motion_man = FdsnMotionManager()

        dataselect_url = FdsnDataselectManager(
            'NL', 'DBN', '2018-11-18T12:00:00'
        ).get_dataselect_url()

        motion_data, ws_url = fdsn_motion_man.get_event_details(
            event_id, network_code, station_code, True
        )
        chart_psa, chart_sd = self.get_spectra_charts(motion_data.stations[0])

        if motion_data:
            context['station_data'] = motion_data.stations[0]
        else:
            context['motion_data'] = None

        context['chart_psa'] = chart_psa
        context['chart_sd'] = chart_sd
        context['ws_url'] = ws_url
        context['dataselect_url'] = dataselect_url

        return context

    def get_spectra_charts(self, station_data):
        try:
            if not station_data:
                return None, None

            data_psa = defaultdict(dict)
            data_sd = defaultdict(dict)
            chart_data_psa = {}
            chart_data_sd = {}

            for sc in station_data.sensor_channels:
                for sa_psa in filter(
                    lambda x: x.type.lower() == 'psa', sc.spectral_amplitudes
                ):
                    data_psa[sc.channel_code][sa_psa.period] = sa_psa.amplitude
                for sa_sd in filter(
                    lambda x: x.type.lower() == 'sd', sc.spectral_amplitudes
                ):
                    data_sd[sc.channel_code][sa_sd.period] = sa_sd.amplitude

            for key in data_psa:
                _tmp = sorted(data_psa[key].items())
                chart_data_psa[key] = _tmp

            for key in data_sd:
                _tmp = sorted(data_sd[key].items())
                chart_data_sd[key] = _tmp

            chart_psa = {
                'exporting': {
                    'chartOptions': {
                        'plotOptions': {
                            'series': {
                                'dataLabels': {
                                    'enabled': 'true'
                                }
                            },
                        }
                    },
                    'fallbackToExportServer': 'false'
                },
                'tooltip': {
                    'headerFormat': '<b>{series.name}</b><br>',
                    'pointFormat': '<b>Spectral period [s]:</b> {point.x}<br><b>PSA [cm/s^2]:</b> {point.y}'
                },
                'chart': {'type': 'scatter'},
                'plotOptions': {
                    'scatter': {
                        'lineWidth': '1'
                    }
                },
                'title': {'text': 'Pseudo-Spectral Acceleration'},
                'xAxis': {
                    'title': {
                        'text': 'Spectral period [s]'
                    },
                    'type': 'logarithmic',
                },
                'yAxis': {
                    'title': {
                        'text': 'PSA [cm/s^2]'
                    },
                    'type': 'logarithmic'
                },
                'series': []
            }

            chart_sd = {
                'exporting': {
                    'chartOptions': {
                        'plotOptions': {
                            'series': {
                                'dataLabels': {
                                    'enabled': 'true'
                                }
                            }
                        }
                    },
                    'fallbackToExportServer': 'false'
                },
                'tooltip': {
                    'headerFormat': '<b>{series.name}</b><br>',
                    'pointFormat': '<b>Spectral period [s]:</b> {point.x}<br><b>SD [cm]:</b> {point.y}'
                },
                'chart': {'type': 'scatter'},
                'plotOptions': {
                    'scatter': {
                        'lineWidth': '1'
                    }
                },
                'title': {'text': 'Spectral Displacement Data'},
                'xAxis': {
                    'title': {
                        'text': 'Spectral period [s]'
                    },
                    'type': 'logarithmic'
                },
                'yAxis': {
                    'title': {
                        'text': 'SD [cm]'
                    },
                    'type': 'logarithmic'
                },
                'series': []
            }

            for t in chart_data_psa:
                chart_psa['series'].append({
                    'name': t,
                    'data': chart_data_psa[t]
                })

            for t in chart_data_sd:
                chart_sd['series'].append({
                    'name': t,
                    'data': chart_data_sd[t]
                })

            dump_psa = json.dumps(chart_psa)
            dump_sd = json.dumps(chart_sd)
            return dump_psa, dump_sd
        except Exception as e:
            self.log_exception(e)
            return None, None


def search_events(request):
    if request.method == 'POST':
        form = SearchEventsForm(request.POST)
        if form.is_valid():
            data, ws_url = FdsnMotionManager().get_event_list(
                event_id=form.cleaned_data['event_id'],
                date_start=form.cleaned_data['date_start'],
                date_end=form.cleaned_data['date_end'],
                magnitude_min=form.cleaned_data['magnitude_min'],
                network_code=form.cleaned_data['network_code'],
                station_code=form.cleaned_data['station_code'],
                event_lat_min=form.cleaned_data['event_lat_min'],
                event_lat_max=form.cleaned_data['event_lat_max'],
                event_lon_min=form.cleaned_data['event_lon_min'],
                event_lon_max=form.cleaned_data['event_lon_max']
            )

            return render(
                request,
                'events.html',
                {
                    'motion_data': data,
                    'breadcrumb': 'Search result (events)',
                    'ws_url': ws_url,
                    'is_homepage': True
                }
            )
        else:
            return render(
                request,
                'search.html',
                {
                    'form': form,
                    'show_info': True
                }
            )
    else:
        form = SearchEventsForm(instance=SearchEvent())
        return render(
            request,
            'search.html',
            {
                'form': form,
                'show_info': True
            }
        )


def search_peak_motions(request):
    if request.method == 'POST':
        form = SearchPeakMotionsForm(request.POST)
        if form.is_valid():
            pga_min, pga_max, pgv_min, pgv_max = \
                RrsmHelpers().pga_pgv_centimeters_to_meters(
                    form.cleaned_data['pga_min'],
                    form.cleaned_data['pga_max'],
                    form.cleaned_data['pgv_min'],
                    form.cleaned_data['pgv_max'])

            data, ws_url = FdsnMotionManager().get_stations_list(
                pga_min=pga_min,
                pga_max=pga_max,
                pgv_min=pgv_min,
                pgv_max=pgv_max
            )

            return render(
                request,
                'stations.html',
                {
                    'motion_data': data,
                    'breadcrumb': 'Search result (peak motions)',
                    'ws_url': ws_url,
                    'is_homepage': True
                }
            )
        else:
            return render(
                request,
                'search.html',
                {
                    'form': form
                }
            )
    else:
        form = SearchPeakMotionsForm(instance=SearchPeakMotions())
        return render(
            request,
            'search.html',
            {
                'form': form
            }
        )


def search_combined(request):
    if request.method == 'POST':
        form = SearchCombinedForm(request.POST)
        if form.is_valid():
            pga_min, pga_max, pgv_min, pgv_max = \
                RrsmHelpers().pga_pgv_centimeters_to_meters(
                    form.cleaned_data['pga_min'],
                    form.cleaned_data['pga_max'],
                    form.cleaned_data['pgv_min'],
                    form.cleaned_data['pgv_max'])

            if form.cleaned_data['pga_min']:
                pga_min = form.cleaned_data['pga_min'] / 100
            if form.cleaned_data['pga_max']:
                pga_max = form.cleaned_data['pga_max'] / 100
            if form.cleaned_data['pgv_min']:
                pgv_min = form.cleaned_data['pgv_min'] / 100
            if form.cleaned_data['pgv_max']:
                pgv_max = form.cleaned_data['pgv_max'] / 100
            data, ws_url = FdsnMotionManager().get_stations_list(
                pga_min=pga_min,
                pga_max=pga_max,
                pgv_min=pgv_min,
                pgv_max=pgv_max
            )

            data, ws_url = FdsnMotionManager().get_stations_list(
                magnitude_min=form.cleaned_data['magnitude_min'],
                pga_min=form.cleaned_data['pga_min'],
                pga_max=form.cleaned_data['pga_max'],
                pgv_min=form.cleaned_data['pgv_min'],
                pgv_max=form.cleaned_data['pgv_max'],
                stat_lat_min=form.cleaned_data['stat_lat_min'],
                stat_lat_max=form.cleaned_data['stat_lat_max'],
                stat_lon_min=form.cleaned_data['stat_lon_min'],
                stat_lon_max=form.cleaned_data['stat_lon_max'],
                event_lat_min=form.cleaned_data['event_lat_min'],
                event_lat_max=form.cleaned_data['event_lat_max'],
                event_lon_min=form.cleaned_data['event_lon_min'],
                event_lon_max=form.cleaned_data['event_lon_max']
            )

            return render(
                request,
                'stations.html',
                {
                    'motion_data': data,
                    'breadcrumb': 'Search result (combined)',
                    'ws_url': ws_url,
                    'is_homepage': True
                }
            )
        else:
            return render(
                request,
                'search.html',
                {
                    'form': form,
                    'show_info': True
                }
            )
    else:
        form = SearchCombinedForm(instance=SearchCombined())
        return render(
            request,
            'search.html',
            {
                'form': form,
                'show_info': True
            }
        )


def search_custom(request):
    if request.method == 'POST':
        form = SearchCustomForm(request.POST)
        if form.is_valid():
            pga_min, pga_max, pgv_min, pgv_max = \
                RrsmHelpers().pga_pgv_centimeters_to_meters(
                    form.cleaned_data['pga_min'],
                    form.cleaned_data['pga_max'],
                    form.cleaned_data['pgv_min'],
                    form.cleaned_data['pgv_max'])

            data, ws_url = FdsnMotionManager().get_stations_list(
                event_id=form.cleaned_data['event_id'],
                date_start=form.cleaned_data['date_start'],
                date_end=form.cleaned_data['date_end'],
                magnitude_min=form.cleaned_data['magnitude_min'],
                network_code=form.cleaned_data['network_code'],
                station_code=form.cleaned_data['station_code'],
                pga_min=pga_min,
                pga_max=pga_max,
                pgv_min=pgv_min,
                pgv_max=pgv_max,
                stat_lat_min=form.cleaned_data['stat_lat_min'],
                stat_lat_max=form.cleaned_data['stat_lat_max'],
                stat_lon_min=form.cleaned_data['stat_lon_min'],
                stat_lon_max=form.cleaned_data['stat_lon_max'],
                event_lat_min=form.cleaned_data['event_lat_min'],
                event_lat_max=form.cleaned_data['event_lat_max'],
                event_lon_min=form.cleaned_data['event_lon_min'],
                event_lon_max=form.cleaned_data['event_lon_max']
            )

            return render(
                request,
                'stations.html',
                {
                    'motion_data': data,
                    'breadcrumb': 'Search result (custom)',
                    'ws_url': ws_url,
                    'is_homepage': True
                }
            )
        else:
            return render(
                request,
                'search_custom.html',
                {
                    'form': form
                }
            )
    else:
        form = SearchCustomForm(instance=SearchCustom())
        return render(
            request,
            'search_custom.html',
            {
                'form': form
            }
        )


def download_waveforms(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        return HttpResponse(
            urls,
            content_type="text/plain"
        )
    else:
        return None


def custom_404(request, exception=None):
    """HTTP 404 custom handler."""
    return render(request, '404.html', {'exception': exception})


def custom_500(request, exception=None):
    """HTTP 500 custom handler."""
    return render(request, '500.html', {'exception': exception})
