# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen
import gzip

from django.db import transaction
from django.shortcuts import get_object_or_404

from .base_classes import NSMAP, NO_FDSNWS_DATA, \
    NodeWrapper, Events, EventWrapper
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

    def get_recent_events(self, days_back):
        try:
            response = self.fdsn_request(
                self.node_wrapper.build_url_events_starttime(days_back)
            )

            if not response:
                return

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

                tmp = event.find('.//mw:magnitude', namespaces=NSMAP).get('publicID')
                if tmp is not None:
                    ew.magnitude_public_id = self.validate_string(tmp)

                tmp = event.find('.//mw:magnitude//mw:mag//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.magnitude_value = self.validate_string(tmp.text)

                tmp = event.find('.//mw:origin', namespaces=NSMAP).get('publicID')
                if tmp is not None:
                    ew.origin_public_id = self.validate_string(tmp)

                tmp = event.find('.//mw:origin//mw:time//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_time = self.validate_string(tmp.text)

                tmp = event.find('.//mw:origin//mw:longitude//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_longitude = self.validate_string(tmp.text)

                tmp = event.find('.//mw:origin//mw:latitude//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_latitude = self.validate_string(tmp.text)

                tmp = event.find('.//mw:origin//mw:depth//mw:value', namespaces=NSMAP)
                if tmp is not None:
                    ew.origin_depth = self.validate_string(tmp.text)

                tmp = event.find('.//mw:preferredOriginID', namespaces=NSMAP)
                if tmp is not None:
                    ew.preferred_origin_id = self.validate_string(tmp.text)

                tmp = event.find('.//mw:preferredMagnitudeID', namespaces=NSMAP)
                if tmp is not None:
                    ew.preferred_magnitude_id = self.validate_string(tmp.text)

                event_graph.events.append(ew)

            return event_graph
        except:
            raise


class FdsnMotionManager(FdsnHttpBase):
    def __init__(self):
        super(FdsnMotionManager, self).__init__()
        self.node_wrapper = NodeWrapper(FdsnNode.objects.get(pk='ODC'))

    def get_event_details(self, event_public_id):
        try:
            pass
        except:
            raise


class FdsnManager(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()