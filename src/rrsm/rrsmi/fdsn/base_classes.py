import json
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta

from obspy.geodetics.flinnengdahl import FlinnEngdahl

NO_FDSNWS_DATA = 'n/a'
NSMAP = {'mw': 'http://quakeml.org/xmlns/bed/1.2'}


# Single node instance wrapper
class NodeWrapper(object):
    def __init__(self, node):
        self.pk = node.pk
        self.code = node.code
        self.description = node.description
        self.url_event = node.url_event
        self.url_motion = node.url_motion

    def build_url_events(
        self, days_back, event_id, date_start, date_end, magnitude_min,
            network_code, station_code, level):

        query = '?'

        if days_back is not None and len(str(days_back)) > 0:
            date_then = datetime.now() - timedelta(days=days_back)
            query += 'starttime={}-{}-{}'.format(
                date_then.year,
                date_then.month,
                date_then.day
                )

        if event_id is not None and len(str(event_id)) > 0:
            query += '&eventid={}'.format(event_id)

        if date_start is not None and len(str(date_start)) > 0:
            query += '&starttime={}-{}-{}'.format(
                date_start.year,
                date_start.month,
                date_start.day
                )

        if date_end is not None and len(str(date_end)) > 0:
            query += '&endttime={}-{}-{}'.format(
                date_end.year,
                date_end.month,
                date_end.day
                )

        if magnitude_min is not None and len(str(magnitude_min)) > 0:
            query += '&minmagnitude={}'.format(magnitude_min)

        if network_code is not None and len(str(network_code)) > 0:
            query += '&network={}'.format(network_code)

        if station_code is not None and len(str(station_code)) > 0:
            query += '&station={}'.format(station_code)

        if level is not None and len(str(level)) > 0:
            query += '&level={}'.format(level)

        return self.url_event + query

    def build_url_event_by_id(self, id):
        return self.url_event + '?eventid={}'.format(id)

    def build_url_motion(self, event_public_id):
        return self.url_motion + '?eventid={}'.format(event_public_id)


class Events(object):
    def __init__(self):
        self.events = []


class EventWrapper(object):
    def __init__(self):
        self.public_id = NO_FDSNWS_DATA
        self.author = NO_FDSNWS_DATA
        self.magnitude_public_id = NO_FDSNWS_DATA
        self.magnitude_value = 0
        self.magnitude_type = NO_FDSNWS_DATA
        self.origin_public_id = NO_FDSNWS_DATA
        self.origin_time = NO_FDSNWS_DATA
        self.origin_longitude = NO_FDSNWS_DATA
        self.origin_latitude = NO_FDSNWS_DATA
        self.origin_depth = 0
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


class MotionDataStation(object):
    def __init__(self):
        self.event_id = NO_FDSNWS_DATA
        self.event_time = NO_FDSNWS_DATA
        self.event_magnitude = NO_FDSNWS_DATA
        self.event_type = NO_FDSNWS_DATA
        self.event_depth = NO_FDSNWS_DATA
        self.event_latitude = NO_FDSNWS_DATA
        self.event_longitude = NO_FDSNWS_DATA
        self.network_code = NO_FDSNWS_DATA
        self.station_code = NO_FDSNWS_DATA
        self.location_code = NO_FDSNWS_DATA
        self.station_latitude = NO_FDSNWS_DATA
        self.station_longitude = NO_FDSNWS_DATA
        self.station_elevation = NO_FDSNWS_DATA
        self.epicentral_distance = NO_FDSNWS_DATA
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


class MotionDataStationChannel(object):
    def __init__(self):
        self.channel_code = NO_FDSNWS_DATA
        self.pga_value = NO_FDSNWS_DATA
        self.pgv_value = NO_FDSNWS_DATA
        self.sensor_azimuth = NO_FDSNWS_DATA
        self.sensor_dip = NO_FDSNWS_DATA
        self.sensor_depth = NO_FDSNWS_DATA
        self.sensor_unit = NO_FDSNWS_DATA
        self.corner_freq_lower = NO_FDSNWS_DATA
        self.corner_freq_upper = NO_FDSNWS_DATA
