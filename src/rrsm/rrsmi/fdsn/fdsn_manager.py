# -*- coding: utf-8 -*-
import gzip
import json
import xml.etree.ElementTree as ET
from urllib import error as urllib_error
from urllib.request import Request, urlopen

from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.conf import settings

from .base_classes import (
    NSMAP,
    NO_FDSNWS_DATA,
    NodeWrapper,
    RoutingWrapper,
    DataselectWrapper,
    MotionData,
    MotionDataStation,
    MotionDataStationChannel,
    SpectralAmplitude,
)

from ..logger import RrsmLoggerMixin

OUTLIER_FILTERING_ENABLED = (
    getattr(settings, "OUTLIER_FILTERING_ENABLED", "False").lower() == "true"
)
PGA_MIN = float(getattr(settings, "PGA_MIN", 0))
PGA_MAX = float(getattr(settings, "PGA_MAX", 0))
PGV_MIN = float(getattr(settings, "PGV_MIN", 0))
PGV_MAX = float(getattr(settings, "PGV_MAX", 0))
PGV_BROADBAND_MIN = float(getattr(settings, "PGV_BROADBAND_MIN", 0))
PGV_BROADBAND_MAX = float(getattr(settings, "PGV_BROADBAND_MAX", 0))
RATIO_PGAX_PGAY_MIN = float(getattr(settings, "RATIO_PGAX_PGAY_MIN", 0))
RATIO_PGAX_PGAY_MAX = float(getattr(settings, "RATIO_PGAX_PGAY_MAX", 0))
RATIO_PGAX_PGAZ_MIN = float(getattr(settings, "RATIO_PGAX_PGAZ_MIN", 0))
RATIO_PGAX_PGAZ_MAX = float(getattr(settings, "RATIO_PGAX_PGAZ_MAX", 0))
RATIO_PGAY_PGAZ_MIN = float(getattr(settings, "RATIO_PGAY_PGAZ_MIN", 0))
RATIO_PGAY_PGAZ_MAX = float(getattr(settings, "RATIO_PGAY_PGAZ_MAX", 0))


class FdsnHttpBase(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnHttpBase, self).__init__()

    def fdsn_request(self, url):
        try:
            req = Request(url)
            req.add_header("Accept-Encoding", "gzip")
            response = urlopen(req)

            if response.info().get("Content-Encoding") == "gzip":
                return gzip.decompress(response.read())
            else:
                return response.read()
        except urllib_error.HTTPError as e:
            self.log_exception(e)
            return None

    def validate_string(self, string):
        if not string or len(string) <= 0:
            return NO_FDSNWS_DATA
        else:
            return string


class FdsnMotionManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnMotionManager, self).__init__()
        self.node_wrapper = NodeWrapper()

    def get_simple_event_list(self, days_back=None):
        """Get simple, top level event list."""
        try:
            ws_url = self.node_wrapper.build_url_simple_events(days_back)

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            data = json.loads(response.decode("utf-8"))
            extracted = self._extract_data(data, False, True)

            return extracted, ws_url
        except Exception as e:
            self.log_exception(e)
            return None, ws_url

    def get_event_list(
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
        """Get list of events including all parameters."""
        try:
            ws_url = self.node_wrapper.build_url_events(
                days_back,
                event_id,
                date_start,
                date_end,
                magnitude_min,
                network_code,
                station_code,
                pga_min,
                pga_max,
                pgv_min,
                pgv_max,
                event_lat_min,
                event_lat_max,
                event_lon_min,
                event_lon_max,
                stat_lat_min,
                stat_lat_max,
                stat_lon_min,
                stat_lon_max,
            )

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            data = json.loads(response.decode("utf-8"))
            extracted = self._extract_data(data, False, True)

            return extracted, ws_url
        except Exception as e:
            self.log_exception(e)
            return None, ws_url

    def get_stations_list(
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
        try:
            ws_url = self.node_wrapper.build_url_events(
                days_back,
                event_id,
                date_start,
                date_end,
                magnitude_min,
                network_code,
                station_code,
                pga_min,
                pga_max,
                pgv_min,
                pgv_max,
                event_lat_min,
                event_lat_max,
                event_lon_min,
                event_lon_max,
                stat_lat_min,
                stat_lat_max,
                stat_lon_min,
                stat_lon_max,
            )

            response = self.fdsn_request(ws_url)

            if not response:
                return None, ws_url

            data = json.loads(response.decode("utf-8"))
            extracted = self._extract_data(data, True, False)

            return extracted, ws_url
        except Exception as e:
            self.log_exception(e)
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

            data = json.loads(response.decode("utf-8"))
            extracted = self._extract_data(data, True, False)

            return extracted, ws_url
        except Exception as e:
            self.log_exception(e)
            return None, ws_url

    def _extract_data(self, data, extract_channels=True, unique_event_id=False):
        try:
            result = MotionData()

            for s in data:
                if unique_event_id is True:
                    if any(x.event_id == s["event-id"] for x in result.stations):
                        continue

                station_data = MotionDataStation()
                if "event-id" in s:
                    station_data.event_id = s["event-id"]
                if "event-time" in s:
                    station_data.event_time = s["event-time"]
                if "event-magnitude" in s:
                    station_data.event_magnitude = s["event-magnitude"]
                if "magnitude-type" in s:
                    station_data.magnitude_type = s["magnitude-type"]
                if "event-depth" in s:
                    station_data.event_depth = s["event-depth"]
                if "event-latitude" in s:
                    station_data.event_latitude = s["event-latitude"]
                if "event-longitude" in s:
                    station_data.event_longitude = s["event-longitude"]
                if "network-code" in s:
                    station_data.network_code = s["network-code"]
                if "station-code" in s:
                    station_data.station_code = s["station-code"]
                if "location-code" in s:
                    station_data.location_code = s["location-code"]
                if "station-latitude" in s:
                    station_data.station_latitude = s["station-latitude"]
                if "station-longitude" in s:
                    station_data.station_longitude = s["station-longitude"]
                if "station-elevation" in s:
                    station_data.station_elevation = s["station-elevation"]
                if "epicentral-distance" in s:
                    station_data.epicentral_distance = s["epicentral-distance"]

                if "event-location-reference" in s:
                    station_data.event_location_reference = s[
                        "event-location-reference"
                    ]
                if "event-magnitude-reference" in s:
                    station_data.event_magnitude_reference = s[
                        "event-magnitude-reference"
                    ]

                if "network-code" in s and "station-code" in s and "event-time" in s:
                    station_data.dataselect_url = FdsnDataselectManager(
                        s["network-code"], s["station-code"], s["event-time"]
                    ).get_dataselect_url()

                if extract_channels is True:
                    for d in s["sensor-channels"]:

                        pga_value_invalid = self._is_channel_outlier(
                            "pga", d["channel-code"], d["pga-value"]
                        )

                        pgv_value_invalid = self._is_channel_outlier(
                            "pgv", d["channel-code"], d["pgv-value"]
                        )

                        ch = MotionDataStationChannel()
                        ch.channel_code = d["channel-code"]
                        ch.pga_value = d["pga-value"] if not pga_value_invalid else 0.0
                        ch.pgv_value = d["pgv-value"] if not pgv_value_invalid else 0.0
                        ch.sensor_azimuth = d["sensor-azimuth"]
                        ch.sensor_dip = d["sensor-dip"]
                        ch.sensor_depth = d["sensor-depth"]
                        ch.low_cut_corner = d["low-cut-corner"]
                        ch.high_cut_corner = d["high-cut-corner"]
                        ch.dataselect_url = FdsnDataselectManager(
                            s["network-code"],
                            s["station-code"],
                            s["event-time"],
                            d["channel-code"],
                        ).get_dataselect_url()

                        if "spectral-amplitudes" in d:
                            for spa in d["spectral-amplitudes"]:
                                sa = SpectralAmplitude()
                                sa.period = spa["period"]
                                sa.amplitude = spa["amplitude"] / 100
                                sa.type = spa["type"]
                                ch.spectral_amplitudes.append(sa)

                        # If one of the values is not valid, do not include
                        # it in the set of sensor channels
                        if not pga_value_invalid and not pgv_value_invalid:
                            station_data.sensor_channels.append(ch)
                        else:
                            self.log_warning(
                                f"Channel does not contain valid values: {ch}"
                            )

                    comps = self._get_station_components(station_data)
                    if comps:
                        station_data.peak_motion_params_invalid = (
                            self._components_invalid(comps)
                        )
                    else:
                        station_data.components_incomplete = True

                result.stations.append(station_data)

            if extract_channels:
                result.stations = [
                    x for x in result.stations if len(x.sensor_channels) > 0
                ]

            return result
        except Exception as e:
            self.log_exception(e)
            return None

    def _is_channel_outlier(self, type, channel, value):
        if not OUTLIER_FILTERING_ENABLED:
            return False

        if channel.lower().startswith("bh"):
            # It is a broadband sensor
            if type == "pga" and (value < PGA_MIN or value > PGA_MAX):
                return True
            if type == "pgv" and (
                value < PGV_BROADBAND_MIN or value > PGV_BROADBAND_MAX
            ):
                return True
        else:
            # It is NOT a broadband sensor
            if type == "pga" and (value < PGA_MIN or value > PGA_MAX):
                return True
            if type == "pgv" and (value < PGV_MIN or value > PGV_MAX):
                return True

        # Checks passed
        return False

    def _get_station_components(self, station_data: MotionDataStation):
        X = list(
            filter(lambda x: x.channel_code.endswith("Z"), station_data.sensor_channels)
        )
        Y = list(
            filter(lambda x: x.channel_code.endswith("N"), station_data.sensor_channels)
        )
        Z = list(
            filter(lambda x: x.channel_code.endswith("E"), station_data.sensor_channels)
        )

        if len(X) and len(Y) and len(Z):
            return {"X": X[0], "Y": Y[0], "Z": Z[0]}
        else:
            return None

    def _components_invalid(self, components):
        """Check ratios of peak motion parameters to determine if station is an outlier.

        Args:
            components (tuple): Station components
        """
        xy = components["X"].pga_value / components["Y"].pga_value
        xz = components["X"].pga_value / components["Z"].pga_value
        yz   = components["Y"].pga_value / components["Z"].pga_value

        if (
            not (RATIO_PGAX_PGAY_MIN < xy < RATIO_PGAX_PGAY_MAX)
            or not (RATIO_PGAX_PGAZ_MIN < xz < RATIO_PGAX_PGAZ_MAX)
            or not (RATIO_PGAY_PGAZ_MIN < yz < RATIO_PGAY_PGAZ_MAX)
        ):
            self.log_warning(
                f"Ratio of peak motion parameters ratio incorrect: {components=}"
            )
            return True

        return False


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
        dt = parse_datetime(self.event_time)
        event_start = dt - timedelta(minutes=1)
        event_end = dt + timedelta(minutes=10)
        event_start_iso = event_start.isoformat().split("+")[0]
        event_end_iso = event_end.isoformat().split("+")[0]

        ws_url = self.routing_wrapper.build_url_routing(
            self.net_code, self.stat_code, event_start_iso, event_end_iso
        )

        response = self.fdsn_request(ws_url)

        if not response:
            return None

        data = json.loads(response.decode("utf-8"))
        dataselect_url = self.dataselect_wrapper.build_url_dataselect(
            data[0]["url"],
            self.net_code,
            self.stat_code,
            event_start_iso,
            event_end_iso,
            self.channel,
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


class FdsnManager(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()
