#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'


class ModuleSupport(object):
    """
    Check if router is available for auto upgrade firmware
    or setting DNS
    """

    UPGRADED_SUPPORT_TYPES = dict()
    # UPGRADE_SUPPORT_TYPE sample
    # ['scan_plugin_name', 'firmware_version', 'hardware_version', 'upgrade_plugin_name', 'firmware_file_path']
    UPGRADED_SUPPORT_TYPES['TP-LINK'] = [('tp_link_wr', '', '', 'tp_link_wr', '')]

    # DNSSET_SUPPORT_TYPE sample
    # ['scan_plugin_name', 'dnsset_plugin_name']
    DNSSET_SUPPORT_TYPES = dict()
    DNSSET_SUPPORT_TYPES['TP-LINK'] = [('tp_link_wr', 'tp_link_wr')]

    def __init__(self):
        pass

    @classmethod
    def dns_set_method(cls, router_plugin_info):
        if router_plugin_info.find(':') > 0:
            vendor = router_plugin_info.split(':')[0]
            scan_plugin = router_plugin_info.split(':')[1]
            if vendor in cls.DNSSET_SUPPORT_TYPES:
                support_list = cls.DNSSET_SUPPORT_TYPES[vendor]
                for support_tuple in support_list:
                    if support_tuple[0] == scan_plugin:
                        return support_tuple[1]
        return None

    @classmethod
    def upgrade_set_method(cls, router_plugin_info, firmware_version, hardware_version):
        if router_plugin_info.find(':') > 0:
            vendor = router_plugin_info.split(':')[0]
            scan_plugin = router_plugin_info.split(':')[1]
            if vendor in cls.UPGRADED_SUPPORT_TYPES:
                support_list = cls.UPGRADED_SUPPORT_TYPES[vendor]
                for support_tuple in support_list:
                    if support_tuple[0] == scan_plugin and cls.version_check(firmware_version, hardware_version,
                                                                             support_tuple[1], support_tuple[2]):
                        # return router upgrade method and firmware path
                        return support_tuple[3], support_tuple[4]
        return None

    @staticmethod
    def version_check(firmware_version, hardware_version, support_firmware_version, support_hardware_version):
        pass
