# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from urllib.request import Request, urlopen
import gzip

from django.db import transaction
from django.shortcuts import get_object_or_404

from .base_classes import NSMAP, NO_FDSNWS_DATA, NodeWrapper, EventWrapper
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

    
    def get_last_week_events(self):
        try:
            response = self.fdsn_request(
                self.node_wrapper.build_url_events_starttime(7)
            )

            if not response:
                return

            root = ET.fromstring(response)

            events = []

            for event in root.findall('.//mw:event', namespaces=NSMAP):
                ew = EventWrapper

                tmp = event.get('publicID')
                if tmp != None:
                    ew.public_id = self.validate_string(tmp)

                tmp = event.find(
                    './/mw:creationInfo//mw:author', namespaces=NSMAP
                )
                if tmp != None:
                    ew.author = self.validate_string(tmp.text)
                    print(ew.author)
                

        except:
            raise


class FdsnManager(RrsmLoggerMixin):
    def __init__(self):
        super(FdsnManager, self).__init__()