#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan
# @Date:   2015-08-13 14:18:37
# @Last Modified by:   tan
# @Last Modified time: 2015-08-18 16:51:59

import requests
from requests.sessions import Session
from requests.auth import AuthBase
import socket
import re
import base64

class Error_port(Exception):
    """自定义的端口错误类"""
    def __init__(self):
        self.value = 'illegal port number'
    def __str__(self):
        return repr(self.value)

class Error_addr(Exception):
    """自定义的IP错误类"""
    def __init__(self):
        self.value = 'illegal ip address'
    def __str__(self):
        return repr(self.value)

class Error_router_offline(Exception):
    """自定义的I路由器离线错误，目标地址不可达"""
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

    #路由器类型常量，用于选择登录方式
    ROUTER_TYPE = {'BASE_AUTH': 0, 'COOKIE': 1}

    #路由器种类常量
    ROUTER_BRAND = {'TP-LINK': 0, 'DD-WRT': 1, 'D-LINK': 2, 'UNKNOW': 3}

    header = {
                b'User-Agent': b'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 
                b'Accept-Language': b'en-US',
                b'Referer': '',
                b'Cookie': ''
            }


    @staticmethod 
    def valid_ip(address):
        """验证IP是否合法"""
        try: 
            socket.inet_aton(address)
            return True
        except:
            return False

    @staticmethod 
    def htm_decode(r):
        """由于requests对中文网页解码不佳，所以用该函数检测响应编码并解码"""
        content = r.content
        if r.encoding != None:
            if r.encoding.lower() != 'utf-8':
                charset = re.compile(r'content="text/html;.?charset=(.*?)"').findall(content)
                #print charset, r.encoding.lower(), r.headers['content-type']
            try:
                if len(charset)>0 and charset[0].lower()!=r.encoding.lower():
                    content = content.decode('gbk').encode('utf-8')
                    return content
            except:
                pass
        return r.text



    def __init__(self, addr, port = 80, name='admin', passwd = 'admin'):
        """初始化路由器信息，包括router_name， router_passwd， router_addr， router_port"""
        self.router_name = name
        self.router_passwd = passwd
        self.router_addr = addr
        if (0 < port and port < 65432):
            self.router_port = port
        else:
            raise Error_port
        if (RouterCrawler.valid_ip(addr)):
            self.addr = addr
        else:
            raise Error_addr
            #self.addr = addr

    def detialCrawl(self, fm_re, hm_re, dns_re, raw):
        """进一步在抓取固件版本，硬件版本，DNS等信息，基于正则表达式匹配"""
        fm_version = ''
        hm_version = ''
        dns = ''

        if (fm_re[0] != ''):
            fm_pattern = re.compile(fm_re[0], re.I | re.S)
            fm_match = fm_pattern.search(raw)
            if fm_match:
                fm_version = fm_match.group(fm_re[1])

        if (hm_re[0] != ''):
            hm_pattern = re.compile(hm_re[0], re.I | re.S)
            hm_match = hm_pattern.search(raw)
            if hm_match:
                hm_version = hm_match.group(hm_re[1])

        if (dns_re[0] != ''):
            dns_pattern = re.compile(dns_re[0], re.I | re.S)
            dns_match = dns_pattern.search(raw)
            if dns_match:
                dns = dns_match.group(dns_re[1])

        return fm_version, hm_version, dns

    def typeRec(self, fingerprint, raw):
        """区分路由器品牌，决定抓取方式，目前支持TP-Link, D-Link, DD-WRT"""
        tp_re = 'TP[\W]?LINK'
        ddwrt_re = 'DD[\W]?WRT'
        dlink_re = 'D[\W]?LINK'
        #print raw

        #注意，DD-WRT必须出现在TP-Link或其他品牌之前，因为DD-WRT中包含其他品牌型号，导致识别错误
        ddwrt_pattern = re.compile(ddwrt_re, re.I)
        match = ddwrt_pattern.search(fingerprint)
        if match:
            return self.ROUTER_BRAND['DD-WRT']
        else:
            match = ddwrt_pattern.search(raw)
            if match:
                return self.ROUTER_BRAND['DD-WRT']

        tp_pattern = re.compile(tp_re, re.I)
        match = tp_pattern.search(fingerprint)
        if match:
            return self.ROUTER_BRAND['TP-LINK']
        else:
            match = tp_pattern.search(raw)
            if match:
                return self.ROUTER_BRAND['TP-LINK']

        dlink_pattern = re.compile(dlink_re, re.I)
        match = dlink_pattern.search(fingerprint)
        if match:
            return self.ROUTER_BRAND['D-LINK']
        else:
            match = dlink_pattern.search(raw)
            if match:
                return self.ROUTER_BRAND['D-LINK']

        return self.ROUTER_BRAND['UNKNOW']
        #return self.ROUTER_BRAND['TP-LINK']

    def tplinkCrawl(self, s, router_info, url):
        cookie = base64.b64encode(self.router_name + ':' + self.router_passwd)
        self.header['Cookie'] = 'Authorization=Basic ' + cookie
        #self.header['Cookie'] = 'tLargeScreenP=1; subType=pcSub; Authorization=Basic YWRtaW46MTIzNDU2'
        for x in xrange(3):
            try:
                r = s.get(url + '/userRpm/StatusRpm.htm', auth = (self.router_name, self.router_passwd) , timeout = 5, allow_redirects = True, headers = self.header)
                break
            except Exception, e:
                router_info['status'] = 'crwaling timeout'
                return
        if (r.status_code == 401):
            print 'Wrong username/passwd!'
        else:
            router_info['username'] = self.router_name
            router_info['passwd'] = self.router_passwd
            router_info['status'] = 'success'

            #fm_re = [r'var statusPara = new Array\(\n(.+?\n){5}"(.+?)"', 2]
            fm_re = [r'var statusPara.+?"(.+?)"', 1]
            hm_re = [r'var statusPara.+?".+?".+?"(.+?)"', 1]
            dns_re = [r'var wanPara(.+?)"([\d\.]+? , [\d\.]+?)"', 2]
            print r.content
            fm, hm, dns = self.detialCrawl(fm_re, hm_re, dns_re, r.content)
            router_info['fm_version'] = fm
            router_info['hm_version'] = hm
            router_info['dns'] = dns

    def ddwrtCrawl(self, s, router_info, url):
        r = s.get(url, timeout = 3, allow_redirects = True, headers = self.header)
        """DD-WRT"""
        fm_re = [r'openAboutWindow.+?>(.+?)</a>', 1]
        hm_re = [r'>Capture\(status_router.sys_model.+?\n(.+?)&nbsp;', 1]
        dns_re = [r'', 0]

        fm, hm, dns = self.detialCrawl(fm_re, hm_re, dns_re, r.content)
        router_info['fm_version'] = fm
        router_info['hm_version'] = hm
        router_info['dns'] = dns        


    def crawl(self, type = ROUTER_TYPE['BASE_AUTH']):
        #构造路由器地址
        url = 'http://' + self.router_addr + ':' + str(self.router_port)
        print url
        self.header['Referer'] = url
        router_info = {
                'url': url,
                'status': '',
                'router_server': '',
                'router_realm': '',
                'username': '',
                'passwd': '',
                'fm_version': '',
                'hm_version': '',
                'dns': ''
                }
        s = Session()
        try:
            r = s.get(url, timeout = 3, allow_redirects = True, headers = self.header)
        except Exception, e:
            #print self.router_addr + ': Timeout!'
            print e
            router_info['status'] = 'connec timeout'
        else:
            #print r.headers
            if 'server' in r.headers:
                router_server = r.headers['server']
                #print router_server
                router_info['router_server'] = router_server
            if 'www-authenticate' in r.headers:
                router_realm = r.headers['www-authenticate']
                #print router_realm
                router_info['router_realm'] = router_realm

            #利用返回头部中的server和www-authenticate字段对路由器类型进行基本识别，再采取相应的抓取方法进行抓取
            fingerprint = router_info['router_server'] + ' ' + router_info['router_realm']
            if (fingerprint != ''):
                router_type = self.typeRec(fingerprint, r.content)
                #print router_type
                if router_type == self.ROUTER_BRAND['TP-LINK']:
                    self.tplinkCrawl(s, router_info, url)
                elif router_type == self.ROUTER_BRAND['DD-WRT']:
                    self.ddwrtCrawl(s, router_info, url) 
        finally:
            return router_info
            pass
            #print r.content

if __name__ == '__main__':
    """测试用例"""
    test_addr = '192.168.1.253'
    test_port = 80
    test_name = 'admin'
    test_passwd = '123456'

    test_router_info_grab = RouterCrawler(addr = test_addr, port = test_port, name = test_name, passwd = test_passwd)
    ret = test_router_info_grab.crawl()
    for (k, v) in ret.items():
        print '%s = ' % k, v
