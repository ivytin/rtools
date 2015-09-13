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
    router_info['addr'] = addr
    router_info['port'] = port
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
        pass

    def produce(self):
        try:
            type, server, realm= TypeRecognition.type_recognition(self.router_info['addr'], self.router_info['port'], self.session)
        except ErrorTimeout, e:
            self.router_info['status'] = 'offline'
            return
        else:
            if server != '':
                self.router_info['server'] = server
            if realm != '':
                self.router_info['realm'] = realm

        crawler_module = __import__(type)
        try:
            crawler = crawler_module.Crawler(self.router_info['addr'], self.router_info['port'], self.try_username, self.try_password, self.session)
        except ErrorPassword, e:
            self.router_info['status'] = 'wrong password'
            return
        crawler.get_info()
