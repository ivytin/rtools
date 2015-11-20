#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'
import threading

import requests
import re

class DnssetFactory(object):
    """produce sepcifical type dns setter"""
    printLock = threading.Lock()

    def print_with_lock(self, str):
        self.printLock.acquire()
        print str
        self.printLock.release()

    def __init__(self, addr, port, username, password, original_dns, type, dns, debug=False):
        self.try_username = username
        self.try_passwd = password
        self.session = requests.session()

        self.addr = addr
        self.port = port
        self.type = type
        self.original_dns = original_dns
        self.dns = dns
        self.debug = debug

    def produce(self):
        dns_1st_re = '\d+\.\d+\.\d+\.\d+'
        original_dns_match = re.compile(dns_1st_re).search(self.original_dns)
        if original_dns_match:
            self.original_dns = original_dns_match.group(0)
        else:
            self.print_with_lock(self.addr + ': fail, find no original dns')
            return
        dns = [self.dns, self.original_dns]
        dnsset_module = __import__(self.type)
        setter = dnsset_module.DnsSetter(self.addr, self.port, self.try_username, self.try_passwd, self.session, self.debug)
        setter.dns_set(dns)

if __name__ == '__main__':
    """Test DNS setter factory"""
    test = DnssetFactory('192.168.1.1', 80, 'admin', 'admin', 'tp_link_wr', ['202.120.2.101', '202.121.2.101'])
    test.produce()
