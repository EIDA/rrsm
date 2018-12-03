# -*- coding: utf-8 -*-
import gzip
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen

from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime

from .base_classes import NSMAP, NO_FDSNWS_DATA, \
    NodeWrapper, RoutingWrapper, DataselectWrapper, \
    MotionData, MotionDataStation, MotionDataStationChannel, SpectralAmplitude

from ..logger import RrsmLoggerMixin


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


class FdsnMotionManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnMotionManager, self).__init__()
        self.node_wrapper = NodeWrapper()

    def get_event_list(
        self, days_back=None, event_id=None, date_start=None, date_end=None,
            magnitude_min=None, network_code=None, station_code=None,
            pga_min=None, pga_max=None, pgv_min=None, pgv_max=None,
            event_lat_min=None, event_lat_max=None,
            event_lon_min=None, event_lon_max=None,
            stat_lat_min=None, stat_lat_max=None,
            stat_lon_min=None, stat_lon_max=None):
        try:
            ws_url = self.node_wrapper.build_url_events(
                days_back, event_id, date_start, date_end,
                magnitude_min, network_code, station_code,
                pga_min, pga_max, pgv_min, pgv_max,
                event_lat_min, event_lat_max,
                event_lon_min, event_lon_max,
                stat_lat_min, stat_lat_max,
                stat_lon_min, stat_lon_max)

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            data = json.loads(response.decode('utf-8'))
            extracted = self._extract_data(data, False, True)

            return extracted, ws_url
        except:
            self.log_exception()
            return None, ws_url

    def get_event_details(
        self, event_public_id, network=None, station=None, spectra=False
    ):
        try:
            ws_url = self.node_wrapper.build_url_motion(
                event_public_id, network, station, spectra
            )

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            data = json.loads(response.decode('utf-8'))
            extracted = self._extract_data(data, True, False)
            
            return extracted, ws_url
        except:
            self.log_exception()
            return None, ws_url

    def _extract_data(
        self, data, extract_channels=True, unique_event_id=False
    ):
        try:
            result = MotionData()

            for s in data:
                if unique_event_id is True:
                    if any(
                        x.event_id == s['event-id'] for x in result.stations
                    ):
                        continue

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
                station_data.dataselect_url = FdsnDataselectManager(
                    s['network-code'],
                    s['station-code'],
                    s['event-time']
                ).get_dataselect_url()

                if extract_channels == True:
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
                        ch.dataselect_url = FdsnDataselectManager(
                            s['network-code'],
                            s['station-code'],
                            s['event-time'],
                            d['channel-code']
                        ).get_dataselect_url()

                        if 'spectral-amplitudes' in d:
                            for spa in d['spectral-amplitudes']:
                                sa = SpectralAmplitude()
                                sa.period = spa['period']
                                sa.amplitude = spa['amplitude']
                                sa.type = spa['type']
                                ch.spectral_amplitudes.append(sa)

                        station_data.sensor_channels.append(ch)
                result.stations.append(station_data)
            return result
        except:
            self.log_exception()
            return None


class FdsnDataselectManager(FdsnHttpBase):
    def __init__(self, net_code, stat_code, event_time, channel=None):
        super(FdsnDataselectManager, self).__init__()
        self.routing_wrapper = RoutingWrapper()
        self.dataselect_wrapper = DataselectWrapper()
        self.net_code = net_code
        self.stat_code = stat_code
        self.event_time = event_time
        self.channel = channel

    def get_dataselect_url(self):
        ws_url = self.routing_wrapper.build_url_routing(
            self.net_code, self.stat_code
        )

        response = self.fdsn_request(ws_url)

        if not response:
            return None

        dt = parse_datetime(self.event_time)
        event_start = dt - timedelta(minutes=1)
        event_end = dt + timedelta(minutes=10)

        data = json.loads(response.decode('utf-8'))
        dataselect_url = self.dataselect_wrapper.build_url_dataselect(
            data[0]['url'],
            self.net_code,
            self.stat_code,
            event_start.isoformat().split('+')[0],
            event_end.isoformat().split('+')[0],
            self.channel
        )

        return dataselect_url


class FdsnWaveformManager(object):
    def __init__(self):
        super(FdsnWaveformManager, self).__init__()
        self.node_wrapper = NodeWrapper()

    def get_waveform_url(self, id):
        ws_url = self.node_wrapper.build_url_waveform_by_id(id)
        return ws_url


class FdsnShakemapManager(object):
    def __init__(self):
        super(FdsnShakemapManager, self).__init__()
        self.node_wrapper = NodeWrapper()

    def get_shakemap_url(self, id):
        ws_url = self.node_wrapper.build_url_shakemap_by_id(id)
        return ws_url


class OdcApiManager(FdsnHttpBase):
    def __init__(self, motion_data_station):
        super(OdcApiManager, self).__init__()

        self.mds = motion_data_station

        dt = parse_datetime(self.mds.event_time)
        event_start = dt - timedelta(seconds=15)
        event_end = dt + timedelta(minutes=3)

        self.api_url = motion_data_station.build_url_odc_api(
            event_start.isoformat().split('+')[0],
            event_end.isoformat().split('+')[0]
        )

    def get_waveform_data(self):
        print(self.api_url)
        response = self.fdsn_request(self.api_url)

        if not response:
            return None

        return json.loads(response.decode('utf-8'))


class FdsnManager(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()
