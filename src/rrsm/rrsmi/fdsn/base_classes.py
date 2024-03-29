# -*- coding: utf-8 -*-
import json
import decimal
from django.conf import settings
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta

from obspy.geodetics.flinnengdahl import FlinnEngdahl

URL_EVENT = getattr(settings, "URL_EVENT", "")
URL_RRSM_EVENT = getattr(settings, "URL_RRSM_EVENT", "")
URL_MOTION = getattr(settings, "URL_MOTION", "")
URL_SHAKEMAP = getattr(settings, "URL_SHAKEMAP", "")
URL_WAVEFORM = getattr(settings, "URL_WAVEFORM", "")
URL_ROUTING = getattr(settings, "URL_ROUTING", "")
URL_ODC_API = getattr(settings, "URL_ODC_API", "")

NO_FDSNWS_DATA = None
NSMAP = {"mw": "http://quakeml.org/xmlns/bed/1.2"}
PGA_PGV_DECIMAL_PLACES = 2


class FdsnBaseClass(object):
    def string_to_decimal(self, string, multiplier=1, decimals=2):
        try:
            tmp = float(string) * multiplier
            casted = decimal.Decimal(tmp)
            result = casted.quantize(decimal.Decimal(10) ** -decimals)
            return result
        except Exception as e:
            raise e


class RoutingWrapper(object):
    def __init__(self):
        self.url_routing = URL_ROUTING

    def build_url_routing(self, network_code, station_code, start=None, end=None):
        payload = {}
        payload["network"] = network_code
        payload["station"] = station_code
        payload["service"] = "dataselect"
        payload["format"] = "json"

        if start:
            payload["start"] = start

        if end:
            payload["end"] = end

        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}?{}".format(self.url_routing, payload_str)


class DataselectWrapper(object):
    def build_url_dataselect(
        self, url, network_code, station_code, event_start, event_end, channel=None
    ):
        payload = {}
        payload["network"] = network_code
        payload["station"] = station_code
        payload["start"] = event_start
        payload["end"] = event_end

        if channel:
            payload["channel"] = channel

        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}?{}".format(url, payload_str)


# Single node instance wrapper
class NodeWrapper(object):
    def __init__(self):
        self.url_event = URL_EVENT
        self.url_rrsm_event = URL_RRSM_EVENT
        self.url_motion = URL_MOTION
        self.url_shakemap = URL_SHAKEMAP
        self.url_waveform = URL_WAVEFORM

    def build_url_simple_events(self, days_back=None):
        """Build URL to get list of events from RRSM"""

        payload = {}
        if days_back is not None and len(str(days_back)) > 0:
            date_then = datetime.now() - timedelta(days=days_back)
            payload["starttime"] = "{}-{}-{}".format(
                date_then.year, date_then.month, date_then.day
            )

        # This is to prevent the encoding of special
        # characters by the requests module
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}?{}".format(self.url_rrsm_event, payload_str)

    def build_url_events(
        self,
        days_back=None,
        event_id=None,
        date_start=None,
        date_end=None,
        magnitude_min=None,
        network_code=None,
        station_code=None,
        pga_min=None,
        pga_max=None,
        pgv_min=None,
        pgv_max=None,
        event_lat_min=None,
        event_lat_max=None,
        event_lon_min=None,
        event_lon_max=None,
        stat_lat_min=None,
        stat_lat_max=None,
        stat_lon_min=None,
        stat_lon_max=None,
    ):
        """Build URL to get list of events including stations, channels, streams
        and peak motion values.
        """

        payload = {}
        if days_back is not None and len(str(days_back)) > 0:
            date_then = datetime.now() - timedelta(days=days_back)
            payload["starttime"] = "{}-{}-{}".format(
                date_then.year, date_then.month, date_then.day
            )

        if event_id is not None and len(str(event_id)) > 0:
            payload["eventid"] = event_id

        if date_start is not None and len(str(date_start)) > 0:
            payload["starttime"] = "{}-{}-{}".format(
                date_start.year, date_start.month, date_start.day
            )

        if date_end is not None and len(str(date_end)) > 0:
            payload["endtime"] = "{}-{}-{}".format(
                date_end.year, date_end.month, date_end.day
            )

        if magnitude_min is not None and len(str(magnitude_min)) > 0:
            payload["minmagnitude"] = magnitude_min

        if network_code is not None and len(str(network_code)) > 0:
            payload["network"] = network_code

        if station_code is not None and len(str(station_code)) > 0:
            payload["station"] = station_code

        if pga_min is not None and len(str(pga_min)) > 0:
            payload["minpga"] = pga_min

        if pga_max is not None and len(str(pga_max)) > 0:
            payload["maxpga"] = pga_max

        if pgv_min is not None and len(str(pgv_min)) > 0:
            payload["minpgv"] = pgv_min

        if pgv_max is not None and len(str(pgv_max)) > 0:
            payload["maxpgv"] = pgv_max

        if all(
            d is not None
            for d in [event_lat_min, event_lat_max, event_lon_min, event_lon_max]
        ):
            payload["eventsquareselection"] = "{},{},{},{}".format(
                event_lat_min, event_lat_max, event_lon_min, event_lon_max
            )

        if all(
            d is not None
            for d in [stat_lat_min, stat_lat_max, stat_lon_min, stat_lon_max]
        ):
            payload["stationsquareselection"] = "{},{},{},{}".format(
                stat_lat_min, stat_lat_max, stat_lon_min, stat_lon_max
            )

        # This is to prevent the encoding of special
        # characters by the requests module
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}?{}".format(self.url_motion, payload_str)

    def build_url_motion(
        self, event_public_id, network=None, station=None, spectra=False
    ):
        payload = {}

        if event_public_id is not None and len(str(event_public_id)) > 0:
            payload["eventid"] = event_public_id

        if network is not None and len(str(network)) > 0:
            payload["network"] = network

        if station is not None and len(str(station)) > 0:
            payload["station"] = station

        if spectra:
            payload["level"] = "spectra"

        # This is to prevent the encoding of special
        # characters by the requests module
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}?{}".format(self.url_motion, payload_str)

    def build_url_shakemap_by_id(self, id):
        return self.url_shakemap + "?id={}".format(id)

    def build_url_waveform_by_id(self, id):
        return self.url_waveform + "?eventid={}".format(id)


class MotionData(object):
    def __init__(self):
        self.stations = []

    def get_stations_order_by_epicentral_distance(self):
        return sorted(self.stations, key=lambda x: x.epicentral_distance)


class MotionDataStation(FdsnBaseClass):
    def __init__(self):
        self.url_odc_api = URL_ODC_API
        self.event_id = NO_FDSNWS_DATA
        self.event_time = NO_FDSNWS_DATA
        self.event_magnitude = 0.0
        self.magnitude_type = NO_FDSNWS_DATA
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
        self.event_location_reference = NO_FDSNWS_DATA
        self.event_magnitude_reference = NO_FDSNWS_DATA
        self.sensor_channels = []
        self.dataselect_url = NO_FDSNWS_DATA
        self.peak_motion_params_invalid = False  # Ratios of peak motion params (issue #29)
        self.components_incomplete = False # Not all components present

    def build_url_odc_api(self, event_start, event_end):
        payload = {}
        payload["start"] = event_start
        payload["end"] = event_end
        payload["units"] = "rawdata"

        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return "{}/{}/{}/--/HH*?{}".format(
            self.url_odc_api, self.network_code, self.station_code, payload_str
        )

    def get_public_id(self):
        try:
            return self.event_id
        except:
            return 0

    def parse_origin_time(self):
        try:
            date = parse_datetime(self.event_time)
            return "{0}-{1}-{2} {3}:{4}:{5}".format(
                str(date.year),
                str(date.month).zfill(2),
                str(date.day).zfill(2),
                str(date.hour).zfill(2),
                str(date.minute).zfill(2),
                str(date.second).zfill(2),
            )
        except:
            pass

    def get_flinn_engdahl(self):
        try:
            fe = FlinnEngdahl()
            result = fe.get_region(
                float(self.event_longitude), float(self.event_latitude)
            ).title()
            return result
        except:
            return "unknown"

    def get_magnitude(self):
        return self.string_to_decimal(self.event_magnitude, decimals=1)

    def get_event_latitude(self):
        return self.string_to_decimal(self.event_latitude)

    def get_event_longitude(self):
        return self.string_to_decimal(self.event_longitude)

    def get_station_latitude(self):
        return self.string_to_decimal(self.station_latitude)

    def get_station_longitude(self):
        return self.string_to_decimal(self.station_longitude)

    def get_epicentral_distance(self):
        return self.string_to_decimal(self.epicentral_distance)

    def get_epicentral_distance_int(self):
        return int(self.epicentral_distance)

    def get_max_pga(self):
        try:
            s = sorted(
                self.sensor_channels, key=lambda x: x.pga_value or 0, reverse=True
            )
            cha = s[0].channel_code
            val = s[0].pga_value
            return self.string_to_decimal(val), cha
        except:
            return "", 0.0

    def get_max_pgv(self):
        try:
            s = sorted(
                self.sensor_channels, key=lambda x: x.pgv_value or 0, reverse=True
            )
            cha = s[0].channel_code
            val = s[0].pgv_value
            return self.string_to_decimal(val), cha
        except:
            return "", 0.0

    def get_map_marker_path(self):
        tmp = self.get_max_pga()[0]
        if tmp > 100:
            return "img/markers/triangle-red.png"
        elif tmp > 50:
            return "img/markers/triangle-orange.png"
        elif tmp > 20:
            return "img/markers/triangle-yellow.png"
        elif tmp > 10:
            return "img/markers/triangle-green.png"
        else:
            return "img/markers/triangle-blue.png"


class MotionDataStationChannel(FdsnBaseClass):
    def __init__(self):
        self.channel_code = NO_FDSNWS_DATA
        self.pga_value = 0.0
        self.pgv_value = 0.0
        self.sensor_azimuth = 0.0
        self.sensor_dip = 0.0
        self.sensor_depth = 0.0
        self.low_cut_corner = 0.0
        self.high_cut_corner = 0.0
        self.spectral_amplitudes = []
        self.dataselect_url = NO_FDSNWS_DATA

    def __str__(self):
        return "Channel: {}, PGA: {}, PGV: {}, URL: {}".format(
            self.channel_code, self.pga_value, self.pgv_value, self.dataselect_url
        )

    def get_amplitudes_order_by_period(self):
        return sorted(self.spectral_amplitudes, key=lambda x: x.period)

    def get_pga(self):
        if not self.pga_value:
            return None
        return self.string_to_decimal(self.pga_value)

    def get_pgv(self):
        if not self.pgv_value:
            return None
        return self.string_to_decimal(self.pgv_value)

    def get_pga_int(self):
        return int(self.pga_value)

    def get_pgv_int(self):
        return int(self.pgv_value)

    def get_low_cut_corner(self):
        return self.low_cut_corner
        # return self.string_to_decimal(self.low_cut_corner)

    def get_high_cut_corner(self):
        return self.high_cut_corner
        # return self.string_to_decimal(self.high_cut_corner)


class SpectralAmplitude(object):
    def __init__(self):
        self.period = 0.0
        self.amplitude = 0.0
        self.type = NO_FDSNWS_DATA
