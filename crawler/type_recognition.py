#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import re
from base_crawler import ErrorTimeout


class TypeRecognition(object):
    """Recognize the router type"""
    # attention! DD-WRT must be the first type to match, because if cotains other types' key string
    brand_res = [
         ('DD-WRT', 'DD\W?WRT'),
         ('TP-LINK', 'TP\W?LINK'), ('TP-LINK', 'TL-'),
         ('D-LINK', 'D\W?LINK'), ('D-LINK', 'DSL'), ('D-LINK', 'DCS'), ('D-LINK', 'DI-\d'),
         ('ASUS', 'RT-'),
         ('Linksys', 'WRT'), ('Linksys', 'Linksys'),
         ('Mecury', 'Wireless N Router MW'),
         ('Tenda', '11N wireless broadband router'), ('Tenda', 'Tenda'), ('Tenda', 'NAT router'),
         ['Surecom', 'Broadband Router'], ('Edimax', 'Default: admin/1234'),
         ('Cisco', 'X2000'),
         ('Netgear', 'Netgear')
    ]

    type_res = dict()
    type_res['DD-WRT'] = [
        ['DD\W?WRT', 'dd_wrt']
    ]
    type_res['TP-LINK'] = [
        ['TL-WR', 'tp_link_wr'],
        ['LINK.+?WR', 'tp_link_wr'],
        ['LINK.+?3G/4G', 'tp_link_wr'],
        ['LINK.+?Gigabit', 'tp_link_vpn_router'],
        ['SOHO', 'tp_link_soho']
    ]
    type_res['D-LINK'] = [
        ['252', 'd_link_dsl2520'],
        ['dcs', 'd_link_dcs'],
        ['D-LINK SYSTEMS, INC.(.+?)location.href = "login_real.htm"', 'd_link_dir505'],
        ['DI-5', 'd_link_di5'],
        ['DI-6', 'd_link_di6']
    ]
    type_res['ASUS'] = [
        ['RT', 'asus_rt', 'asus_rt_2']
    ]
    type_res['Linksys'] = [
        ['E1200', 'linksys_e'],
        ['WRT', 'linksys_wrt']
    ]
    type_res['Mecury'] = [
        ['Wireless N Router MW', 'mecury_wm']
    ]
    type_res['Tenda'] = [
        ['NAT router', 'tenda'],
        ['11N wireless broadband router', 'tenda'],
        ['tenda', 'tenda']
    ]
    type_res['Surecom'] = [
        ['Broadband Router', 'surecom']
    ]
    type_res['Cisco'] = [
        ['X2000', 'cisco_x2000']
    ]
    type_res['Netgear'] = [
        ['jwnr2000', 'netgear_jwnr2000', 'netgear_jwnr2000_2'],
        ['Netgear', 'netgear_wnr1']
        # ['WGR', 'netgear_wgr6', 'netgear_wnr1'],
        # ['WNR', 'netgear_wnr1', 'netgear_wgr6']
    ]
    type_res['Edimax'] = [
        ['Default: admin/1234', 'edimax']
    ]

    server = ''
    realm = ''

    def connect(self, session, url, times):
        for x in xrange(times):
            try:
                r = session.get(url, timeout=3, allow_redirects=True)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def type_recognition(self, addr, port, session):
        url = 'http://' + addr + ':' + str(port)
        r = self.connect(session, url, 1)
        if 'server' in r.headers:
            self.server = r.headers['server']
        if 'www-authenticate' in r.headers:
            self.realm = r.headers['www-authenticate']
        fingerprint_str = self.server + self.realm + r.content
        for brand_re in self.brand_res:
            brand_pattern = re.compile(brand_re[1], re.I)
            brand_match = brand_pattern.search(fingerprint_str)
            if brand_match:
                type_re_list = self.type_res[brand_re[0]]
                for type_re in type_re_list:
                    type_pattern = re.compile(type_re[0], re.S | re.I)
                    brand_match = type_pattern.search(fingerprint_str)
                    if brand_match:
                        return type_re, self.server, self.realm
        return '', self.server, self.realm
