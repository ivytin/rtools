#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import base64
import re
from base_crawler import BaseCrawler
from base_crawler import ErrorTimeout
from base_crawler import ErrorPassword


class Crawler(BaseCrawler):
    """crawler for Surecom serial routers"""
    def __init__(self, addr, port, username, password, session):
        BaseCrawler.__init__(self, addr, port, username, password, session)
        self.res['dns'] = ['/Comm/Status.js', 'var va_DNSServer.+?(".+?".+?".+?")', 1]

        self.headers = {
            b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            b'Accept-Language': b'en-US',
            b'Referer': '',
                        }
        self.url = 'http://' + self.addr + ':' + str(port)

    def get_info(self):
        dns_info = ''
        r = self.connect_auth_with_headers(self.url, 1)

        if r.status_code == 403:
            raise ErrorPassword

        dns_url = 'http://' + self.addr + ':' + str(self.port) + self.res['dns'][0]
        self.headers['Referer'] = self.url
        try:
            r = self.connect_auth_with_headers(dns_url, 1)
        except ErrorTimeout, e:
            pass
        else:
            dns_pattern = re.compile(self.res['dns'][1], re.I | re.S)
            dns_match = dns_pattern.search(r.content)
            if dns_match:
                dns_info = dns_match.group(self.res['dns'][2])

        return dns_info, '', 'Surecom'

if __name__ == '__main__':
    """Test this unit"""
    req = __import__('requests')
    crawler = Crawler('192.168.0.1', 80, 'admin', 'admin', req.session, True)
    crawler.get_info()
