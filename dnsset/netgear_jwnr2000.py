#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import re
import requests
from base_setter import BaseSetter
from base_setter import ErrorTimeout


class DnsSetter(BaseSetter):
    """DNS auto setter for Netgear JWNR2000 serial routers"""

    def __init__(self, addr, port, username, password, session, debug):
        BaseSetter.__init__(self, addr, port, username, password, session, debug)

        self.headers = {
            b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            b'Accept-Language': b'en-US',
            b'Referer': '',
        }
        self.base_url = 'http://' + self.addr + ':' + str(port)

    def get_now_info(self):

        bas_ether_url = self.base_url + '/BAS_ether.htm'
        bas_ether_ref = self.base_url + '/BAS_basic.htm'
        self.headers[b'Referer'] = bas_ether_ref
        r = self.connect_auth_with_headers(bas_ether_url, 3)
        return r.content

    def generate_payload(self, content, dns):
        dyna_payload = dict()
        dyna_payload['head'] = "submit_flag=ether&" \
                               "conflict_wanlan=&" \
                               "change_wan_type=1&" \
                               "run_test=no&" \
                               "domain_name=&" \
                               "WANAssign=dhcp&" \
                               "DNSAssign=1" \
                               "flush_flag=0&" \
                               "Apply=Apply&" \
                               "loginreq=dhcp"
        dyna_payload['sys_name'] = '&system_name='
        dyna_payload['ether_ip'] = "&ether_ipaddr="
        dyna_payload['ether_subnet'] = '&ether_subnet='
        dyna_payload['ether_gateway'] = '&ether_gateway='
        dyna_payload['ether_dnsaddr1'] = '&ether_dnsaddr1='
        dyna_payload['ether_dnsaddr2'] = '&ether_dnsaddr2='
        dyna_payload['mtu'] = '&hid_mtu_value='
        dyna_payload['mac_assign'] = '&MACAssign='
        dyna_payload['spoof_mac'] = '&Spoofmac='

        dyna_re = dict()
        dyna_pattern = dict()
        dyna_match = dict()
        dyna_re['ether_dnsaddr1'] = 'ether_get_dns1="(.+?)"'
        dyna_re['ether_dnsaddr2'] = 'ether_get_dns2="(.+?)"'
        dyna_re['ether_ip'] = 'var old_wan_ip="(.+?)"'
        dyna_re['ether_subnet'] = 'ether_get_subnet="(.+?)"'
        dyna_re['ether_gateway'] = 'ether_get_gateway="(.+?)"'
        dyna_re['sys_name'] = 'name="system_name" size="20" maxlength="60" value="(.+?)"'
        dyna_re['mtu'] = "var wan_mtu_now='(.+?)'"

        dyna_re['spoof_mac'] = 'var ether_get_this_mac="(.+?)"'
        dyna_re['mac_assign'] = "var ether_get_mac_assign='(.+?)'"

        for key, val in dyna_re.iteritems():
            item_pattern = re.compile(val, re.I)
            dyna_match[key] = item_pattern.search(content).group(1)
            dyna_payload[key] += dyna_match[key]

        if dyna_match['mac_assign'] == '2':
            dyna_payload['spoof_mac'] = dyna_payload['spoof_mac'].replace(':', '%3A')
            return dyna_payload['head'] + dyna_payload['sys_name'] + dyna_payload['ether_ip'] + \
                   dyna_payload['ether_subnet'] + dyna_payload['ether_gateway'] + dyna_payload['ether_dnsaddr1'] + \
                   dyna_payload['ether_dnsaddr2'] + dyna_payload['mtu'] + dyna_payload['mac_assign'] + dyna_payload['spoof_mac']
        else:
            return dyna_payload['head'] + dyna_payload['sys_name'] + dyna_payload['ether_ip'] + \
                   dyna_payload['ether_subnet'] + dyna_payload['ether_gateway'] + dyna_payload['ether_dnsaddr1'] + \
                   dyna_payload['ether_dnsaddr2'] + dyna_payload['mtu'] + dyna_payload['mac_assign'] + dyna_payload['spoof_mac']

    def dns_set(self, dns):
        try:
            self.headers[b'Referer'] = self.base_url
            self.connect_auth_with_headers(self.base_url, 2)
        except ErrorTimeout:
            self.print_with_lock(self.addr + ': connect timout at first try')
            return

        try:
            content = self.get_now_info()
        except ErrorTimeout:
            self.print_with_lock(self.addr + 'connect timeout at get info')
            return
        post_url_re = '<FORM method="POST" action="(.+?)"'
        post_url = self.base_url + re.compile(post_url_re, re.I).search(content).group(1).replace(' ', '%20')
        payload = self.generate_payload(content, dns)
        if self.debug:
            self.print_with_lock('payload: ' + payload)
            self.print_with_lock('url: ' + post_url)

        try:
            r = self.post_auth_with_headers(post_url, payload, 3)
        except ErrorTimeout:
            self.print_with_lock(self.addr + ': connect timeout at post')
            return

        self.print_with_lock(self.addr + ': success')


if __name__ == '__main__':
    """Test this unit"""
    s = requests.session()
    crawler = DnsSetter('192.168.33.1', 80, 'admin', 'password', s, True)
    crawler.dns_set(['8.8.8.8', '5.5.5.5'])
