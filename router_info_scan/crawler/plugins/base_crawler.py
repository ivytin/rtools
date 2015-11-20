#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

from ...http_helper import HttpHelper


class BaseCrawler(object):
    """The base class of all crawler"""
    def __init__(self, addr, port, username, password, session, debug):
        """，including router_name， router_passwd， router_addr， router_port"""
        self.addr = addr
        self.port = port
        self.url = 'http://' + addr + ':' + str(port)
        self.try_username = username
        self.try_passwd = password
        self.session = session
        self.debug = debug

        self.res = dict()
        self.res['dns'] = []
        self.res['firmware'] = []
        self.res['dns'] = []

        self.headers = dict()

    def connect(self, url, times):
        HttpHelper.connect(self.session, url, times)

    def connect_with_headers(self, url, times):
        HttpHelper.connect_with_headers(self.session, url, times, self.headers)

    def connect_auth_with_headers(self, url, times):
        HttpHelper.connect_auth_with_headers(self.session, url, (self.try_username, self.try_passwd), times, self.headers)

    def get_info(self):
        pass

    def get_dns(self):
        pass

    def get_firmware(self):
        pass

    def get_hardware(self):
        pass







