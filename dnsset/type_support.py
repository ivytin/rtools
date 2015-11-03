#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'


class TypeSupport(object):
    """"""

    support_types = dict()
    support_types['TP-LINK'] = [('tp_link_wr', 'tp_link_wr')]

    def __init__(self):
        pass

    @classmethod
    def dns_set_method(cls, router_type):
        if router_type.find(':') > 0:
            brand = router_type.split(':')[0]
            dns_type = router_type.split(':')[1]
            if brand in cls.support_types:
                support_type = cls.support_types[brand]
                for type_tuple in support_type:
                    if type_tuple[0] == dns_type:
                        return type_tuple[1]
        return None
