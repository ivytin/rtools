#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import base64
import re
from base_setter import BaseSetter
from base_setter import ErrorTimeout

class DnsSetter(BaseSetter):
    """DNS auto setter for TP-Link WR serial routers"""
    def __init__(self, addr, port, username, passwd, session):
        BaseSetter.__init__(self, addr, port, username, passwd, session)
        auth_cookie = base64.b64encode(self.try_username + ':' + self.try_passwd)
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
        self.headers['Accept-Language'] = 'en-US',
        self.headers['Referer'] = '',
        self.headers['Cookie'] = 'tLargeScreenP=1; subType=pcSub; Authorization=Basic ' + auth_cookie

        self.wan_type_search = '/userRpm/WanCfgRpm.htm'
        self.dyna_para = '?Save=save&dnsserver=[dns1]&dnsserver2=[dns2]&manual=2&mtu=1500&wantype=0'
        self.dyna_ref = '/userRpm/WanDynamicIpCfgRpm.htm?wan=0'
        self.ppp_para = 'lcpMru=1480&manual=2&dnsserver=[dns1]&dnsserver2=[dns2]&Save=save&Advanced=Advanced'
        self.ppp_ref = '/userRpm/PPPoECfgAdvRpm.htm?Advanced=%B8%DF%BC%B6%C9%E8%D6%C3&wan=0'

    def dns_set(self, dns):
        url = 'http://' + self.addr + ':' + str(self.port) + self.wan_type_search
        self.headers['Referer'] = 'http://' + self.addr + ':' + str(self.port)
        try:
            r = self.connect_auth_with_headers(url, 2)
        except ErrorTimeout, e:
            self.print_with_lock(self.addr + ': fail, connect timeout')
            return

        if r.status_code == 401:
            self.print_with_lock(self.addr + ': fail, wrong password')
            return

        ref_re = 'location.href="(.+?)"'
        ref_re_index = 1
        ref_pattern = re.compile(ref_re, re.I)
        match = ref_pattern.search(r.content)
        if match:
            wan_url = 'http://' + self.addr + ':' + str(self.port) + match.group(ref_re_index)
        else:
            self.print_with_lock(self.addr + ': fail, can not find the wan_url')
            return

        if wan_url.find('WanDynamicIpCfgRpm'):
            payload = self.dyna_payload(dns[0], dns[1])
        elif wan_url.find('PPPoECfgRpm'):
            payload = self.ppp_payload(dns[0], dns[1])
        else:
            self.printLock(self.addr + ': fail, can not find the dns change method in this router')
            return

        dns_url = wan_url + payload
        try:
            r = self.connect_auth_with_headers(dns_url, 2)
        except ErrorTimeout:
            self.print_with_lock(self.addr + ': fail, no response')
        else:
            if r.content.find(dns[0]):
                self.print_with_lock(self.addr + ': success')
            else:
                self.print_with_lock(self.addr + ': fail, change dns fail')

    def dyna_payload(self, dns1, dns2):
        self.headers['Referer'] = 'http://' + self.addr + ':' + str(self.port) + self.dyna_ref
        payload = self.dyna_para.replace('[dns1]', dns1)
        payload = payload.replace('[dns2]', dns2)
        return payload

    def ppp_payload(self, dns1, dns2):
        self.headers['Referer'] = 'http://' + self.addr + ':' + str(self.port) + self.ppp_ref
        payload = self.ppp_para.replace('[dns1]', dns1)
        payload = payload.replace('[dns2]', dns2)
        return payload

if __name__ == '__main__':
    """Test this unit"""
    req = __import__('requests')
    test = DnsSetter('192.168.1.1', 80, 'admin', 'admin', req.session)
