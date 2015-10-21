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
         ('ASUS', 'RT-N'), ('ASUS', 'RT-G'),
         ('Linksys', 'WRT'), ('Linksys', 'Linksys'),
         ('Mecury', 'Wireless N Router MW'),
         ('Tenda', '11N wireless broadband router'), ('Tenda', 'Tenda'), ('Tenda', 'NAT router'),
         ['Surecom', 'Broadband Router'], ('Edimax', 'Default: admin/1234'),
         ('Cisco', 'X2000'),
         ('Netgear', 'Netgear')
    ]

    type_res = dict()
    type_res['DD-WRT'] = [
        ['dd_wrt', 'DD\W?WRT']
    ]
    type_res['TP-LINK'] = [
        ['tp_link_wr', 'TL-WR'],
        ['tp_link_wr', 'LINK.+?WR'],
        ['tp_link_wr', 'LINK.+?3G/4G'],
        ['tp_link_vpn_router', 'LINK.+?Gigabit']
    ]
    type_res['D-LINK'] = [
        ['d_link_dsl2520', '252'],
        ['d_link_dcs', 'dcs'],
        ['d_link_dir505', 'D-LINK SYSTEMS, INC.(.+?)location.href = "login_real.htm"'],
        ['d_link_di5', 'DI-5'],
        ['d_link_di6', 'DI-6']
    ]
    type_res['ASUS'] = [
        ['asus_rt', 'RT-N'],
        ['asus_rt', 'RT-G']
    ]
    type_res['Linksys'] = [
        ['linksys_e', 'E1200'],
        ['linksys_wrt', 'WRT']
    ]
    type_res['Mecury'] = [
        ['mecury_wm', 'Wireless N Router MW']
    ]
    type_res['Tenda'] = [
        ['tenda', 'NAT router'],
        ['tenda', '11N wireless broadband router'],
        ['tenda', 'tenda']
    ]
    type_res['Surecom'] = [
        ['surecom', 'Broadband Router']
    ]
    type_res['Cisco'] = [
        ['cisco_x2000', 'X2000']
    ]
    type_res['Netgear'] = [
        ['netgear_jwnr2000', 'jwnr2000'],
        ['netgear_wgr6', 'WGR'],
        ['netgear_wgr6', 'WNR3500L'],
        ['netgear_wnr1', 'WNR']
    ]
    type_res['Edimax'] = [
        ['edimax', 'Default: admin/1234']
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
        fingerprstr = self.server + self.realm + r.content
        for brand_re in self.brand_res:
            brand_pattern = re.compile(brand_re[1], re.I)
            brand_match = brand_pattern.search(fingerprstr)
            if brand_match:
                type_re_list = self.type_res[brand_re[0]]
                for type_re in type_re_list:
                    type_pattern = re.compile(type_re[1], re.S | re.I)
                    brand_match = type_pattern.search(fingerprstr)
                    if brand_match:
                        return type_re[0], self.server, self.realm
        return '', self.server, self.realm
