# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta

from obspy.geodetics.flinnengdahl import FlinnEngdahl

URL_EVENT = getattr(settings, 'URL_EVENT', '')
URL_MOTION = getattr(settings, 'URL_MOTION', '')
URL_SHAKEMAP = getattr(settings, 'URL_SHAKEMAP', '')
URL_WAVEFORM = getattr(settings, 'URL_WAVEFORM', '')

NO_FDSNWS_DATA = None
NSMAP = {'mw': 'http://quakeml.org/xmlns/bed/1.2'}


# Single node instance wrapper
class NodeWrapper(object):
    def __init__(self):
        self.url_event = URL_EVENT
        self.url_motion = URL_MOTION
        self.url_shakemap = URL_SHAKEMAP
        self.url_waveform = URL_WAVEFORM

    def build_url_events(
        self, days_back, event_id, date_start, date_end, magnitude_min,
            network_code, station_code, level):

        query = '?'

        if days_back is not None and len(str(days_back)) > 0:
            date_then = datetime.now() - timedelta(days=days_back)
            query += 'starttime={}-{}-{}&'.format(
                date_then.year,
                date_then.month,
                date_then.day
                )

        if event_id is not None and len(str(event_id)) > 0:
            query += 'eventid={}&'.format(event_id)

        if date_start is not None and len(str(date_start)) > 0:
            query += 'starttime={}-{}-{}&'.format(
                date_start.year,
                date_start.month,
                date_start.day
                )

        if date_end is not None and len(str(date_end)) > 0:
            query += 'endttime={}-{}-{}&'.format(
                date_end.year,
                date_end.month,
                date_end.day
                )

        if magnitude_min is not None and len(str(magnitude_min)) > 0:
            query += 'minmagnitude={}&'.format(magnitude_min)

        if network_code is not None and len(str(network_code)) > 0:
            query += 'network={}&'.format(network_code)

        if station_code is not None and len(str(station_code)) > 0:
            query += 'station={}&'.format(station_code)

        if level is not None and len(str(level)) > 0:
            query += 'level={}&'.format(level)

        return self.url_event + query

    def build_url_event_by_id(self, id):
        return self.url_event + '?eventid={}'.format(id)

    def build_url_motion(self, event_public_id, network=None, station=None, spectra=False):
        query = '?eventid={}'.format(event_public_id)

        if network is not None and len(str(network)) > 0:
            query += '&network={}'.format(network)

        if station is not None and len(str(station)) > 0:
            query += '&station={}'.format(station)

        if spectra:
            query += '&level=spectra'

        return self.url_motion + query

    def build_url_shakemap_by_id(self, id):
        return self.url_shakemap + '?id={}'.format(id)

    def build_url_waveform_by_id(self, id):
        return self.url_waveform + '?id={}'.format(id)


class Events(object):
    def __init__(self):
        self.events = []


class EventWrapper(object):
    def __init__(self):
        self.public_id = NO_FDSNWS_DATA
        self.author = NO_FDSNWS_DATA
        self.magnitude_public_id = NO_FDSNWS_DATA
        self.magnitude_value = 0.0
        self.magnitude_type = NO_FDSNWS_DATA
        self.origin_public_id = NO_FDSNWS_DATA
        self.origin_time = NO_FDSNWS_DATA
        self.origin_longitude = 0.0
        self.origin_latitude = 0.0
        self.origin_depth = 0.0
        self.preferred_origin_id = NO_FDSNWS_DATA
        self.preferred_magnitude_id = NO_FDSNWS_DATA

    def parse_origin_time(self):
        try:
            date = parse_datetime(self.origin_time)
            return '{0}-{1}-{2} {3}:{4}:{5}'.format(
                str(date.year),
                str(date.month).zfill(2),
                str(date.day).zfill(2),
                str(date.hour).zfill(2),
                str(date.minute).zfill(2),
                str(date.second).zfill(2)
            )
        except:
            pass

    def get_public_id(self):
        try:
            return self.public_id.split('/')[2]
        except:
            return 0

    def get_flinn_engdahl(self):
        try:
            fe = FlinnEngdahl()
            result = fe.get_region(
                float(self.origin_longitude), float(self.origin_latitude)
                ).title()
            return result
        except:
            return 'unknown'


class MotionData(object):
    def __init__(self):
        self.stations = []

    def get_stations_order_by_epicentral_distance(self):
        return sorted(self.stations, key=lambda x: x.epicentral_distance)


class MotionDataStation(object):
    def __init__(self):
        self.event_id = NO_FDSNWS_DATA
        self.event_time = NO_FDSNWS_DATA
        self.event_magnitude = 0.0
        self.event_type = NO_FDSNWS_DATA
        self.event_depth = 0.0
        self.event_latitude = 0.0
        self.event_longitude = 0.0
        self.network_code = NO_FDSNWS_DATA
        self.station_code = NO_FDSNWS_DATA
        self.location_code = NO_FDSNWS_DATA
        self.station_latitude = 0.0
        self.station_longitude = 0.0
        self.station_elevation = 0.0
        self.epicentral_distance = 0.0
        self.event_reference = NO_FDSNWS_DATA
        self.sensor_channels = []

    def parse_origin_time(self):
        try:
            date = parse_datetime(self.event_time)
            return '{0}-{1}-{2} {3}:{4}:{5}'.format(
                str(date.year),
                str(date.month).zfill(2),
                str(date.day).zfill(2),
                str(date.hour).zfill(2),
                str(date.minute).zfill(2),
                str(date.second).zfill(2)
            )
        except:
            pass

    def get_max_pga(self):
        try:
            self.sensor_channels.sort(key=lambda x: x.pga_value, reverse=True)
            cha = self.sensor_channels[0].channel_code
            val = self.sensor_channels[0].pga_value
            return val, cha
        except:
            return '', 0

    def get_max_pgv(self):
        try:
            self.sensor_channels.sort(key=lambda x: x.pgv_value, reverse=True)
            cha = self.sensor_channels[0].channel_code
            val = self.sensor_channels[0].pgv_value
            return val, cha
        except:
            return '', 0


class MotionDataStationChannel(object):
    def __init__(self):
        self.channel_code = NO_FDSNWS_DATA
        self.pga_value = 0.0
        self.pgv_value = 0.0
        self.sensor_azimuth = 0.0
        self.sensor_dip = 0.0
        self.sensor_depth = 0.0
        self.sensor_unit = NO_FDSNWS_DATA
        self.corner_freq_lower = 0.0
        self.corner_freq_upper = 0.0
        self.spectral_amplitudes = []

    def get_amplitudes_order_by_period(self):
        return sorted(
            self.spectral_amplitudes, key=lambda x: x.period
        )


class SpectralAmplitude(object):
    def __init__(self):
        self.period = 0.0
        self.amplitude = 0.0
        self.type = NO_FDSNWS_DATA
