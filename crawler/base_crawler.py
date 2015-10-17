#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

class ErrorTimeout(Exception):
    """self define exception: requests page time out"""
    def __init__(self):
        self.value = 'Can not reach destination'

    def __str__(self):
        return repr(self.value)

class ErrorPassword(Exception):
    """self define exception: wrong password"""
    def __init__(self):
        self.value = 'Wrong password'

    def __str__(self):
        return repr(self.value)

class BaseCrawler(object):
    """The base class of all crawler"""
    def __init__(self, addr, port, username, password, session):
        """，包括router_name， router_passwd， router_addr， router_port"""
        self.addr = addr
        self.port = port
        self.url = 'http://' + addr + ':' + str(port)
        self.try_username = username
        self.try_passwd = password
        self.session = session

        self.res = dict()
        self.res['dns'] = []
        self.res['firmware'] = []
        self.res['dns'] = []

        self.headers = dict()

    def connect(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, timeout=3, allow_redirects=True)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def connect_with_headers(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, timeout=3, allow_redirects=True, headers=self.headers)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def connect_auth_with_headers(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, auth=(self.try_username, self.try_passwd),
                                     timeout=3, allow_redirects=True, headers=self.headers)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def get_info(self):
        pass

    def get_dns(self):
        pass

    def get_firmware(self):
        pass

    def get_hardware(self):
        pass







