#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import re
from base_crawler import ErrorTimeout

class TypeRecognition(object):
    """Recognize the router type"""
    # attention! DD-WRT must be the first type to match, because if cotains other types' key string
    brand_res = [('DD-WRT', 'DD\W?WRT'), ('TP-LINK', 'TP\W?LINK'), ('D-LINK', 'D\W?LINK'), ('D-LINK', 'DSL')]

    type_res = dict()
    type_res['DD-WRT'] = []
    type_res['TP-LINK'] = []
    type_res['D-LINK'] = []

    def __init__(self):
        pass

    def connect(self, session, url, times):
        for x in xrange(times):
            try:
                r = session.get(url, timeout=3, allow_redirects=True)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    @staticmethod
    def type_recognition(self, addr, port, session):
        url = 'http://' + addr + ':' + int(port)
        r = self.connect(session, url, 3)
        if 'server' in r.headers:
                server = r.headers['server']
        if 'www-authenticate' in r.headers:
                realm = r.headers['www-authenticate']
        fingerprint = server + realm
        for brand_re in self.brand_res:
            brand_pattern = re.compile(brand_re[1], re.I)
            brand_match = brand_pattern.search(fingerprint)
            if brand_match:
                type_re_list = self.type_res[brand_re[0]]
                for type_re in type_re_list:
                    type_pattern = re.compile(type_re[1], re.S | re.I)
                    brand_match = type_pattern.search(fingerprint)
                    if brand_match:
                        return type_re[0]

        return -1
