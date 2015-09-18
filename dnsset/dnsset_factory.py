#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import requests

class DnssetFactory(object):
    """produce sepcifical type dns setter"""

    def __init__(self, addr, port, username, password, type, dns):
        self.try_username = username
        self.try_passwd = password
        self.session = requests.session()

        self.addr = addr
        self.port = port
        self.type = type
        self.dns = dns

    def produce(self):
        dnsset_module = __import__(self.type)
        setter = dnsset_module.DnsSetter(self.addr, self.port, self.try_username, self.try_passwd, self.session)
        setter.dns_set(self.dns)

if __name__ == '__main__':
    """Test DNS setter factory"""
    test = DnssetFactory('192.168.1.1', 80, 'admin', 'admin', 'tp_link_wr', ['202.120.2.101', '202.121.2.101'])
    test.produce()
