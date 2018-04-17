# -*- coding: utf-8 -*-
import gzip
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen

from .base_classes import NSMAP, NO_FDSNWS_DATA, \
    NodeWrapper, Events, EventWrapper, \
    MotionData, MotionDataStation, MotionDataStationChannel
from ..logger import RrsmLoggerMixin
from ..models import FdsnNode


class FdsnHttpBase(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnHttpBase, self).__init__()

    def fdsn_request(self, url):
        try:
            req = Request(url)
            req.add_header('Accept-Encoding', 'gzip')
            response = urlopen(req)

            if response.info().get('Content-Encoding') == 'gzip':
                return gzip.decompress(response.read())
            else:
                return response.read()
        except Exception:
            self.log_exception(url)
            raise

    def validate_string(self, string):
        if not string or len(string) <= 0:
            return NO_FDSNWS_DATA
        else:
            return string


class FdsnEventManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnEventManager, self).__init__()
        self.node_wrapper = NodeWrapper(FdsnNode.objects.get(pk='ODC'))

    def get_events(
        self, days_back=None, event_id=None, date_start=None, date_end=None,
            magnitude_min=None, network_code=None,
            station_code=None, level=None):
        try:
            ws_url = self.node_wrapper.build_url_events(
                days_back, event_id, date_start, date_end,
                magnitude_min, network_code,
                station_code, level)

            self.log_information(ws_url)

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            root = ET.fromstring(response)
            event_graph = Events()

            for event in root.findall('.//mw:event', namespaces=NSMAP):
                ew = EventWrapper()

                tmp = event.get('publicID')
                if tmp is not None:
                    ew.public_id = self.validate_string(tmp)

                tmp = event.find(
                    './/mw:creationInfo//mw:author', namespaces=NSMAP
                )
                if tmp is not None:
                    ew.author = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:magnitude', namespaces=NSMAP).get('publicID')
                if tmp is not None:
                    ew.magnitude_public_id = self.validate_string(tmp)

                tmp = event.find(
                    './/mw:magnitude//mw:mag//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.magnitude_value = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:origin', namespaces=NSMAP).get('publicID')
                if tmp is not None:
                    ew.origin_public_id = self.validate_string(tmp)

                tmp = event.find(
                    './/mw:origin//mw:time//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_time = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:origin//mw:longitude//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_longitude = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:origin//mw:latitude//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_latitude = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:origin//mw:depth//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_depth = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:preferredOriginID', namespaces=NSMAP)
                if tmp is not None:
                    ew.preferred_origin_id = self.validate_string(tmp.text)

                tmp = event.find(
                    './/mw:preferredMagnitudeID', namespaces=NSMAP)
                if tmp is not None:
                    ew.preferred_magnitude_id = self.validate_string(tmp.text)

                event_graph.events.append(ew)
            return event_graph, ws_url
        except:
            self.log_exception()
            return None, ws_url


class FdsnMotionManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnMotionManager, self).__init__()
        self.node_wrapper = NodeWrapper(FdsnNode.objects.get(pk='ODC'))

    def get_event_details(self, event_public_id):
        try:
            ws_url = self.node_wrapper.build_url_motion(event_public_id)
            self.log_information(
                'Trying to get motion data for event {}'.format(ws_url)
            )

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            result = MotionData()
            data = json.loads(response.decode('utf-8'))

            for s in data:
                station_data = MotionDataStation()
                station_data.event_id = s['event-id']
                station_data.event_time = s['event-time']
                station_data.event_magnitude = s['event-magnitude']
                station_data.event_type = s['event-type']
                station_data.event_depth = s['event-depth']
                station_data.event_latitude = s['event-latitude']
                station_data.event_longitude = s['event-longitude']
                station_data.network_code = s['network-code']
                station_data.station_code = s['station-code']
                station_data.location_code = s['location-code']
                station_data.station_latitude = s['station-latitude']
                station_data.station_longitude = s['station-longitude']
                station_data.station_elevation = s['station-elevation']
                station_data.epicentral_distance = s['epicentral-distance']
                station_data.event_reference = s['event-reference']

                for d in s['sensor-channels']:
                    ch = MotionDataStationChannel()
                    ch.channel_code = d['channel-code']
                    ch.pga_value = d['pga-value']
                    ch.pgv_value = d['pgv-value']
                    ch.sensor_azimuth = d['sensor-azimuth']
                    ch.sensor_dip = d['sensor-dip']
                    ch.sensor_depth = d['sensor-depth']
                    ch.sensor_unit = d['sensor-unit']
                    ch.corner_freq_lower = d['corner-freq-lower']
                    ch.corner_freq_upper = d['corner-freq-upper']
                    station_data.sensor_channels.append(ch)
                result.stations.append(station_data)
            return result, ws_url
        except:
            self.log_exception()
            return None, ws_url


class FdsnManager(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()
