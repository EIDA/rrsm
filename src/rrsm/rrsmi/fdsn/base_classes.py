from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta


NO_FDSNWS_DATA = 'n/a'
NSMAP = {'mw': 'http://quakeml.org/xmlns/bed/1.2'}


# Single node instance wrapper
class NodeWrapper(object):
    def __init__(self, node):
        self.pk = node.pk
        self.code = node.code
        self.description = node.description
        self.url_event = node.url_event

    def build_url_events_starttime(self, days):
        date_then = datetime.now() - timedelta(days=days)
        return self.url_event + '?starttime={}-{}-{}'.format(
            date_then.year,
            date_then.month,
            date_then.day,
            )


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
