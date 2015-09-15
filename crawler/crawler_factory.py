#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import requests
from type_recognition import TypeRecognition
from base_crawler import ErrorTimeout
from base_crawler import ErrorPassword

class CrawlerFactory(object):
    """product specifical type crawler"""

    def __init__(self, addr, port, username, password, debug):
        self.try_username = username
        self.try_password = password
        self.addr = addr


        self.session = requests.session()
        self.router_info = dict()
        self.router_info['addr'] = addr
        self.router_info['port'] = port
        self.router_info['status'] = ''
        self.router_info['server'] = ''
        self.router_info['realm'] = ''
        self.router_info['username'] = ''
        self.router_info['password'] = ''
        self.router_info['firmware'] = ''
        self.router_info['hardware'] = ''
        self.router_info['dns'] = ''
        self.router_info['type'] = ''

        self.debug = debug

    def produce(self):
        recognition = TypeRecognition()
        try:
            type, server, realm = recognition.type_recognition(self.router_info['addr'],
                                                               self.router_info['port'], self.session)
        except ErrorTimeout, e:
            print self.addr + ': fail, connect timeout'
            self.router_info['status'] = 'offline'
            return self.router_info
        else:
            if server:
                self.router_info['server'] = server
            if realm:
                self.router_info['realm'] = realm

        if not type:
            print self.addr + ': fail, unknown type'
            self.router_info['status'] == 'unknown type'
            return self.router_info

        self.router_info['type'] = type
        crawler_module = __import__(type)

        try:
            crawler = crawler_module.Crawler(self.router_info['addr'], self.router_info['port'],
                                             self.try_username, self.try_password, self.session)
            if self.debug:
                print 'requests headers:\n', crawler.headers
        except ErrorTimeout, e:
            print self.addr + ': fail, connect timeout'
            self.router_info['status'] = 'offline'
            return self.router_info

        try:
            dns_info, firmware, hardware = crawler.get_info()
        except ErrorPassword, e:
            print self.addr + ': fail, wrong password'
            self.router_info['status'] = 'wrong password'
        except ErrorTimeout, e:
            print self.addr + ': fail, timeout'
            self.router_info['status'] = 'incomplete'
        else:
            self.router_info['username'] = self.try_username
            self.router_info['password'] = self.try_password
            self.router_info['dns'] = dns_info
            self.router_info['firmware'] = firmware
            self.router_info['hardware'] = hardware
            if dns_info or firmware or hardware:
                print self.addr + ': success'
                self.router_info['status'] = 'success'

            if self.debug:
                print 'router info:\n', self.router_info
                print '\n\n'
        finally:
            return self.router_info

if __name__ == '__main__':
    crawler_factory = CrawlerFactory('192.168.0.1', 80, 'admin', 'admin', True)
    crawler_factory.produce()
