#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import requests
from type_recognition import TypeRecognition
from base_crawler import ErrorTimeout
from base_crawler import ErrorPassword

class CrawlerFactory(object):
    """product specifical type crawler"""
    session = requests.session()
    router_info = dict()
    router_info['addr'] = ''
    router_info['port'] = 0
    router_info['status'] = 'unknow'
    router_info['server'] = ''
    router_info['realm'] = ''
    router_info['realm'] = ''
    router_info['username'] = ''
    router_info['password'] = ''
    router_info['firmware'] = ''
    router_info['hardware'] = ''
    router_info['dns'] = ''

    def __init__(self, addr, port, username, password):
        self.try_username = username
        self.try_password = password

        self.router_info['addr'] = addr
        self.router_info['port'] = port

    def produce(self):
        try:
            type, server, realm = TypeRecognition.type_recognition(self.router_info['addr'], self.router_info['port'], self.session)
        except ErrorTimeout, e:
            self.router_info['status'] = 'offline'
            return self.router_info
        else:
            if server != '':
                self.router_info['server'] = server
            if realm != '':
                self.router_info['realm'] = realm

        if type == -1:
            self.router_info['status'] == 'unknow type'
            return self.router_info

        crawler_module = __import__(type)
        try:
            crawler = crawler_module.Crawler(self.router_info['addr'], self.router_info['port'], self.try_username, self.try_password, self.session)
        except ErrorPassword, e:
            self.router_info['status'] = 'wrong password'
            return self.router_info
        except ErrorTimeout, e:
            self.router_info['status'] = 'offline'
            return self.router_info

        dns_info, firmware, hardware = crawler.get_info()
        self.router_info['dns'] = dns_info
        self.router_info['firmware'] = firmware
        self.router_info['hardware'] = hardware
        if dns_info != '' and firmware != '' and hardware != '':
            self.router_info['status'] = 'success'
        return self.router_info
