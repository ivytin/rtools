#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import base64
import re
from base_crawler import BaseCrawler
from base_crawler import ErrorTimeout
from base_crawler import ErrorPassword


class Crawler(BaseCrawler):
    """crawler for Netgear JWNR serial routers"""
    def __init__(self, addr, port, username, password, session, debug):
        BaseCrawler.__init__(self, addr, port, username, password, session, debug)
        self.res['dns1'] = ['/RST_status.htm', 'var info_get_dns1="(.+?)";']
        self.res['dns2'] = ['/RST_status.htm', 'var info_get_dns2="(.+?)";']
        self.res['firmware'] = ['/RST_status.htm', '<TD nowrap>V([\d\._]+?)</TD>', 1]
        self.res['hardware'] = ['/RST_status.htm', "var product_id='(.+?)';", 1]

        self.headers = {
            b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            b'Accept-Language': b'en-US',
            b'Referer': '',
                        }
        self.url = 'http://' + self.addr + ':' + str(port)

    def get_info(self):
        dns_info = ''
        firmware = ''
        hardware = ''
        r = self.connect_auth_with_headers(self.url, 1)

        if r.status_code == 403:
            raise ErrorPassword

        dns_url = 'http://' + self.addr + ':' + str(self.port) + self.res['dns1'][0]
        self.headers['Referer'] = self.url
        try:
            r = self.connect_auth_with_headers(dns_url, 1)
        except ErrorTimeout, e:
            pass
        else:
            dns_pattern1 = re.compile(self.res['dns1'][1], re.I | re.S)
            dns_match1 = dns_pattern1.search(r.content)
            if dns_match1:
                dns_info += dns_match1.group(1) + ' '
            dns_pattern2 = re.compile(self.res['dns2'][1], re.I | re.S)
            dns_match2 = dns_pattern2.search(r.content)
            if dns_match2:
                dns_info += dns_match2.group(1)

            firmware_pattern = re.compile(self.res['firmware'][1], re.I | re.S)
            firmware_match = firmware_pattern.search(r.content)
            if firmware_match:
                firmware = firmware_match.group(self.res['firmware'][2])

            hardware_pattern = re.compile(self.res['hardware'][1], re.I | re.S)
            hardware_match = hardware_pattern.search(r.content)
            if hardware_match:
                hardware = hardware_match.group(self.res['hardware'][2])

        return dns_info, firmware, hardware

if __name__ == '__main__':
    """Test this unit"""
    req = __import__('requests')
    crawler = Crawler('192.168.0.1', 80, 'admin', 'admin', req.session, True)
    crawler.get_info()
