#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan
# @Date:   2015-08-13 14:18:37
# @Last Modified by:   tan
# @Last Modified time: 2015-08-26 11:36:49

import requests
from requests.sessions import Session
from requests.auth import AuthBase
import socket
import re
import base64
from sqlite_helper import DataHelper
from sqlite_helper import DataCondition


class ErrorRouterOffline(Exception):
    """自定义的路由器离线错误，目标地址不可达"""

    def __init__(self):
        self.value = 'routers offline (can not reach dest)'

    def __str__(self):
        return repr(self.value)


class RouterCrawler(object):
    """Automatic crawl routers' info including version and configure settings"""
    """自动抓取路由器版本以及配置信息"""

    router_name = ''
    router_passwd = ''
    router_addr = ''
    router_port = 0

    router_server = ''
    router_realm = ''
    router_hardware_version = ''
    router_fireware_version = ''

    # 路由器类型常量，用于选择登录方式
    ROUTER_TYPE = {'BASE_AUTH': 0, 'COOKIE': 1}

    # 路由器种类常量
    ROUTER_BRAND = {'TP-LINK': 0, 'DD-WRT': 1, 'D-LINK': 2, 'UNKNOW': 3}

    header = {
        b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
        b'Accept-Language': b'en-US',
        b'Referer': '',
        b'Cookie': ''
    }

    @staticmethod
    def htm_decode(r):
        """由于requests对中文网页解码不佳，所以用该函数检测响应编码并解码"""
        content = r.content
        if r.encoding != None:
            if r.encoding.lower() != 'utf-8':
                charset = re.compile(r'content="text/html;.?charset=(.*?)"').findall(content)
                # print charset, r.encoding.lower(), r.headers['content-type']
            try:
                if len(charset) > 0 and charset[0].lower() != r.encoding.lower():
                    content = content.decode('gbk').encode('utf-8')
                    return content
            except:
                pass
        return r.text

    def __init__(self, addr, port=80, name='admin', passwd='admin', debug=False):
        """初始化路由器信息，包括router_name， router_passwd， router_addr， router_port"""
        self.router_name = name
        self.router_passwd = passwd
        self.router_addr = addr
        self.db = DataHelper("testDB.db")
        self.debug_flag = debug
        self.router_port = port
        self.addr = addr
        self.db.open()

    def reCrawl(self, fm_re, fm_index, hm_re, hm_index, dns_re, dns_index, raw):
        """进一步在抓取固件版本，硬件版本，DNS等信息，基于正则表达式匹配"""
        fm_version = ''
        hm_version = ''
        dns = ''
        if fm_re != '':
            fm_pattern = re.compile(fm_re, re.I | re.S)
            fm_match = fm_pattern.search(raw)
            if fm_match:
                fm_version = fm_match.group(fm_index)

        if hm_re != '':
            hm_pattern = re.compile(hm_re, re.I | re.S)
            hm_match = hm_pattern.search(raw)
            if hm_match:
                hm_version = hm_match.group(hm_index)

        if dns_re != '':
            dns_pattern = re.compile(dns_re, re.I | re.S)
            dns_match = dns_pattern.search(raw)
            if dns_match:
                dns = dns_match.group(dns_index)

        return fm_version, hm_version, dns

    def typeRec(self, fingerprint, raw):
        """区分路由器品牌，决定抓取方式，目前支持TP-Link, D-Link, DD-WRT"""

        router_res = [('DD-WRT', 'DD\W?WRT'), ('TP-LINK', 'TP\W?LINK'), ('D-LINK', 'D\W?LINK'), ('D-LINK', 'DSL')]
        # print raw
        # 注意，DD-WRT必须出现在TP-Link或其他品牌之前，因为DD-WRT中包含其他品牌型号，导致识别错误
        fingerprint = fingerprint + raw
        for m_re in router_res:
            m_pattern = re.compile(m_re[1], re.I)
            match = m_pattern.search(fingerprint)
            if match:
                rs = self.db.table("MODULE_MATCH").select('ID', 'FINGERPRINT').where(
                    DataCondition(("=", "AND"), TYPE_INDEX=self.ROUTER_BRAND[m_re[0]]),
                    DataCondition((">", "AND"), WEIGHT=0)).fetchall()
                for r in rs:
                    r_pattern = re.compile(r[1], re.S | re.I)
                    match = r_pattern.search(fingerprint)
                    if match:
                        return r[0]
                r = self.db.table("MODULE_MATCH").select('ID').where(
                    DataCondition(("=", "AND"), TYPE_INDEX=self.ROUTER_BRAND[m_re[0]]),
                    DataCondition(("=", "AND"), WEIGHT=0)).fetchone()
                return r[0]

        return -1
        # return self.ROUTER_BRAND['TP-LINK']

    def infoCrawl(self, s, r, url, router_info):
        # 'INFO_URL', 'FIREWARE', 'FIREWARE_INDEX', 'HARDWARE',
        # 'HARDWARE_INDEX', 'DNS', 'DNS_INDEX', 'AUTH_COOKIE', 'OTHER_COOKIE', 'REFERER'
        info_url = r[0]
        fm_re = r[1]
        fm_index = r[2]
        hm_re = r[3]
        hm_index = r[4]
        dns_re = r[5]
        dns_index = r[6]
        auth_cookie = r[7]
        other_cookie = r[8]
        referer = r[9]

        auth_cookie += base64.b64encode(self.router_name + ':' + self.router_passwd)
        self.header['Cookie'] = other_cookie + auth_cookie
        if referer == 'url':
            self.header['Referer'] = url
        else:
            self.header['Referer'] = ''

        if self.debug_flag:
            print self.header

        for x in xrange(3):
            try:
                url += info_url
                r = s.get(url, auth=(self.router_name, self.router_passwd), timeout=3, allow_redirects=True,
                          headers=self.header)
                break
            except Exception, e:
                router_info['status'] = 'crwaling timeout'
                # raise e
                return

        if (r.status_code == 401):
            router_info['status'] = 'Wrong username/passwd!'
        else:
            if self.debug_flag:
                print r.content[:100]
            router_id = router_info
            router_info['username'] = self.router_name
            router_info['passwd'] = self.router_passwd
            router_info['status'] = 'success'
            fm, hm, dns = self.reCrawl(fm_re, fm_index, hm_re, hm_index, dns_re, dns_index, r.content)
            router_info['fm_version'] = fm
            router_info['hm_version'] = hm
            router_info['dns'] = dns
            return router_info

    # def ddwrtCrawl(self, s, router_info, url):
    #     r = s.get(url, timeout = 3, allow_redirects = True, headers = self.header)
    #     """DD-WRT"""
    #     fm_re = [r'openAboutWindow.+?>(.+?)</a>', 1]
    #     hm_re = [r'>Capture\(status_router.sys_model.+?\n(.+?)&nbsp;', 1]
    #     dns_re = [r'', 0]

    #     fm, hm, dns = self.reCrawl(fm_re, hm_re, dns_re, r.content)
    #     router_info['fm_version'] = fm
    #     router_info['hm_version'] = hm
    #     router_info['dns'] = dns        

    def crawl(self, type=ROUTER_TYPE['BASE_AUTH']):
        # 构造路由器地址
        url = 'http://' + self.router_addr + ':' + str(self.router_port)
        print url
        router_info = {
            'ip': self.router_addr,
            'port': self.router_port,
            'status': '',
            'router_server': '',
            'router_realm': '',
            'username': '',
            'passwd': '',
            'fm_version': '',
            'hm_version': '',
            'dns': '',
            'type_index': ''
        }
        s = Session()
        try:
            r = s.get(url, timeout=3, allow_redirects=True)
        except Exception, e:
            if self.debug_flag:
                print e
            router_info['status'] = 'connect timeout'
            return router_info
        else:
            # print r.headers
            if 'server' in r.headers:
                router_server = r.headers['server']
                # print router_server
                router_info['router_server'] = router_server
            if 'www-authenticate' in r.headers:
                router_realm = r.headers['www-authenticate']
                # print router_realm
                router_info['router_realm'] = router_realm

            # 利用返回头部中的server和www-authenticate字段对路由器类型进行基本识别，再采取相应的抓取方法进行抓取
            fingerprint = router_info['router_server'] + ' ' + router_info['router_realm']
            # print r.content
            if fingerprint != '' or r.content != '':
                router_id = self.typeRec(fingerprint, r.content)
                if self.debug_flag:
                    print router_id
                if router_id >= 0:
                    router_info['type_index'] = router_id
                    '''对于非常规登录方式路由器必须单独给出登录及信息抓取方式
                    '''
                    if router_id == 50:
                        # D-Link DIR-505
                        router_info['hm_version'] = 'DIR-505'
                        username = base64.b64encode(self.router_name).replace('=', 'A')
                        passwd = base64.b64encode(self.router_passwd).replace('=', 'A')
                        data = 'request=login&admin_user_name=' + username + '&admin_user_pwd=' + passwd + '&user_type=0'
                        try:
                            login = s.post('http://192.168.0.1/my_cgi.cgi?0.7204311818502432', data=data)
                            if login.content.find('default'):
                                router_info['status'] = 'success'
                                router_info['username'] = self.router_name
                                router_info['passwd'] = self.router_passwd
                            else:
                                router_info['status'] = 'wrong passwd'
                        except Exception, e:
                            pass
                        data = 'request=load_settings&table_name=wan_info&table_name=fw_ver&table_name=hw_ver'
                        try:
                            dir_505_info = s.post('http://192.168.0.1/my_cgi.cgi?0.23814993476113056', data=data)
                            r = self.db.table("INFO_MATCH").select(
                                'FIREWARE', 'FIREWARE_INDEX',
                                'HARDWARE', 'HARDWARE_INDEX',
                                'DNS', 'DNS_INDEX',
                            ).where(DataCondition(("=", "AND"), ID=router_id)).fetchone()
                            fm_pattern = re.compile(r[0])
                            match = fm_pattern.search(dir_505_info.content)
                            if match:
                                router_info['fm_version'] = match.group(r[1])

                            hm_pattern = re.compile(r[2])
                            match = hm_pattern.search(dir_505_info.content)
                            if match:
                                router_info['hm_version'] += match.group(r[3])

                            dns_pattern = re.compile(r[4])
                            match = dns_pattern.search(dir_505_info.content)
                            if match:
                                router_info['dns'] = match.group(r[5])
                        except Exception, e:
                            pass
                    else:
                        # 常规路由器
                        r = self.db.table("INFO_MATCH").select('INFO_URL',
                                                               'FIREWARE', 'FIREWARE_INDEX',
                                                               'HARDWARE', 'HARDWARE_INDEX',
                                                               'DNS', 'DNS_INDEX',
                                                               'AUTH_COOKIE', 'OTHER_COOKIE',
                                                               'REFERER'
                                                               ).where(
                            DataCondition(("=", "AND"), ID=router_id)).fetchone()
                        if not r:
                            router_info['status'] = 'unsupport module'
                        else:
                            router_info = self.infoCrawl(s, r, url, router_info)
                else:
                    router_info['status'] = "can't recognize this module"
            else:
                router_info['status'] = "no fingerprint"
        finally:
            if self.debug_flag:
                print router_info
            return router_info
            # print r.content


if __name__ == '__main__':
    """测试用例"""
    test_addr = '192.168.0.1'
    test_port = 80
    test_name = 'admin'
    test_passwd = 'admin'

    test_router_info_grab = RouterCrawler(addr=test_addr, port=test_port,
                                          name=test_name, passwd=test_passwd, debug=True)
    ret = test_router_info_grab.crawl()
    for (k, v) in ret.items():
        print '%s = ' % k, v
