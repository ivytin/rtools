#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import re
from base_crawler import BaseCrawler
from base_crawler import ErrorTimeout

class Crawler(BaseCrawler):
    """crawler for DD-WRT routers"""
    def __init__(self, addr, port, username, password, session, debug=False):
        BaseCrawler.__init__(self, addr, port, username, password, session, debug=False)
        self.res['dns'] = ['/userRpm/StatusRpm.htm', 'var wanPara = new Array(.+?)"([\d\.]+? , [\d\.]+?)"', 2]
        self.res['firmware'] = ['', 'openAboutWindow.+?>(.+?)</a>"', 1]
        self.res['hardware'] = ['', '>Capture\(status_router.sys_model.+?\n(.+?)&nbsp;', 1]

    def get_info(self):
        dns_info = ''
        firmware = ''
        hardware = ''

        dns_url = 'http://' + self.addr + ':' + int(self.port) + self.res['dns'][0]
        try:
            r = self.connect(dns_url, 3)
        except ErrorTimeout, e:
            pass
        else:
            dns_pattern = re.compile(self.res['dns'][1], re.I | re.S)
            dns_match = dns_pattern.search(r.context)
            if dns_match:
                dns_info = dns_match.group(self.res['dns'][2])

        firmware_url = 'http://' + self.addr + ':' + int(self.port) + self.res['firmware'][0]
        if firmware_url == dns_url:
            firmware_pattern = re.compile(self.res['firmware'][1], re.I | re.S)
            firmware_match = firmware_pattern.search(r.context)
            if firmware_match:
                firmware = firmware_match.group(self.res['firmware'][2])
        else:
            try:
                r = self.connect(firmware_url, 3)
            except ErrorTimeout, e:
                pass
            else:
                firmware_pattern = re.compile(self.res['firmware'][1], re.I | re.S)
                firmware_match = firmware_pattern.search(r.context)
                if firmware_match:
                    firmware = firmware_match.group(self.res['firmware'][2])

        hardware_url = 'http://' + self.addr + ':' + int(self.port) + self.res['hardware'][0]
        if hardware_url == firmware_url:
            hardware_pattern = re.compile(self.res['hardware'][1], re.I | re.S)
            hardware_match = hardware_pattern.search(r.context)
            if hardware_match:
                hardware = hardware_match.group(self.res['hardware'][2])
        else:
            try:
                r = self.connect(hardware_url, 3)
            except ErrorTimeout, e:
                pass
            else:
                hardware_pattern = re.compile(self.res['hardware'][1], re.I | re.S)
                hardware_match = hardware_pattern.search(r.context)
                if hardware_match:
                    hardware = hardware_match.group(self.res['hardware'][2])

        return dns_info, firmware, hardware
