#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'tan'

import requests


class UpgradeFactory(object):
    """produce specific type firmware upgrade plugin"""
    def __init__(self, addr, port, username, password, type, firmware, debug=False):
        self.try_username = username
        self.try_passwd = password
        self.session = requests.session()

        self.addr = addr
        self.port = port
        self.type = type
        self.firmware = firmware
        self.debug = debug

    def produce(self):
        upgrade_module = __import__(self.type)
        upgrader = upgrade_module.Upgrader(self.addr, self.port, self.try_username, self.try_passwd, self.session, self.debug)
        upgrader.upgrade()

if __name__ == '__main__':
    """Test DNS setter factory"""
    test = UpgradeFactory('192.168.1.1', 80, 'admin', 'admin', 'tp_link_wr', ['202.120.2.101', '202.121.2.101'])
    test.produce()
