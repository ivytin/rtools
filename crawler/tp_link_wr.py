#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import base64
from base_crawler import BaseCrawler

class Crawler(BaseCrawler):
    def __init__(self):
        self.res['dns'] = ['/userRpm/StatusRpm.htm', 'var wanPara = new Array(.+?)"([\d\.]+? , [\d\.]+?)"']
        self.res['firmware'] = ['/userRpm/StatusRpm.htm', 'var statusPara = new Array.+?"(.+?)"']
        self.res['hardware'] = ['/userRpm/StatusRpm.htm', 'var statusPara = new Array.+?".+?".+?"(.+?)"']

        auth_cookie = base64.b64encode(self.try_username + ':' + self.try_passwd)
        self.headers = {'Cookie': 'tLargeScreenP=1; subType=pcSub; Authorization=Basic ' + auth_cookie,
                        }
