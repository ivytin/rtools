#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import requests
from type_recognition import TypeRecognition
from base_crawler import ErrorTimeout

class CrawlerFactory(object):
    """product specifical type crawler"""
    def __init__(self, addr, port, username, password):
        self.session = requests.session()
        self.router_info['addr'] = addr
        self.router_info['port'] = port
        self.router_info['status'] = 'unknow'
        self.router_info['server'] = ''
        self.router_info['realm'] = ''
        self.router_info['realm'] = ''
        self.router_info['username'] = ''
        self.router_info['password'] = ''
        self.router_info['firmware'] = ''
        self.router_info['hardware'] = ''
        self.router_info['dns'] = ''

    def produce(self):
        try:
            type = TypeRecognition.type_recognition(self.router_info['addr'], self.router_info['port'], self.session)
        except ErrorTimeout, e:
            self.router_info['status'] = 'offline'
            return
        crawler_module = __import__(type)
        crawler = crawler_module.crawler
        #crawler.
