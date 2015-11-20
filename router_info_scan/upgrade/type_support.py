#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'


class UpgradeTypeSupport(object):
    """
    Check if router is available for auto upgrade firmware
    """

    support_types = dict()
    support_types['TP-LINK'] = [('tp_link_wr', '', '', 'tp_link_wr', '')]

    def __init__(self):
        pass

    @classmethod
    def upgrade_set_method(cls, router_type, firmware_version, hardware_version):
        if router_type.find(':') > 0:
            brand = router_type.split(':')[0]
            router_type = router_type.split(':')[1]
            if brand in cls.support_types:
                support_type = cls.support_types[brand]
                for type_tuple in support_type:
                    if type_tuple[0] == router_type and UpgradeTypeSupport.version_check(firmware_version, hardware_version,
                                                                                         type_tuple[1], type_tuple[2]):
                        # return router upgrade method and firmware path
                        return type_tuple[3], type_tuple[4]
        return None

    @staticmethod
    def version_check(firmware_version, hardware_version, support_firmware_version, support_hardware_version):
        pass
