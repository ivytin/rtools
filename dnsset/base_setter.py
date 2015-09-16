#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

class ErrorTimeout(Exception):
    """self define exception: requests page time out"""
    def __init__(self):
        self.value = 'Can not reach destination'

    def __str__(self):
        return repr(self.value)

class ErrorPassword(Exception):
    """self define exception: wrong password"""
    def __init__(self):
        self.value = 'Wrong password'

    def __str__(self):
        return repr(self.value)

class BaseSetter(object):
    """Automatic change routers' dns settings"""

    def __init__(self, addr, port, username, passwd, session):
        self.addr = addr
        self.port = port
        self.try_username = username
        self.try_passwd = passwd
        self.session = session
        self.headers = dict()

    def connect(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, timeout=3, allow_redirects=True)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def connect_with_headers(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, timeout=3, allow_redirects=True, headers=self.headers)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def connect_auth_with_headers(self, url, times):
        for x in xrange(times):
            try:
                r = self.session.get(url, auth=(self.try_username, self.try_passwd),
                                     timeout=3, allow_redirects=True, headers=self.headers)
                return r
            except Exception, e:
                pass
        raise ErrorTimeout

    def dns_set(self, dns):
        pass
