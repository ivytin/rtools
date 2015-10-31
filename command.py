#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan

from optparse import OptionParser
from crawler.crawler_factory import CrawlerFactory
from dnsset.dnsset_factory import DnssetFactory
from thread_pool import WorkManager
import time
import sys
from upgrade.upgrade_factory import UpgradeFactory

default_out_file = time.strftime("%m.%d-%H.%M.%S", time.localtime()) + '.csv'

parser = OptionParser()
# IP address input file
parser.add_option("-i", "--input-file", dest="in_file_path",
                  help="IP address input file path", metavar="FILE")
# result out file
parser.add_option("-o", "--output-file", dest="out_file_path", default=default_out_file,
                  help="scan output file path", metavar="FILE")
# thread number
parser.add_option("-t", "--threads", dest="threads_num", type="int", default=3,
                  help="scan threads num", metavar="NUM")

# crawling mode
parser.add_option("-c", "--crawl",
                  action="store_true", dest="crawl", default=False,  
                  help="enable the crawling mode")

# setting dns mode
parser.add_option("-d", "--dns",
                  action="store_true", dest="dns", default=False,  
                  help="enable the dns set mode")

# crawler debug mode
parser.add_option("--cdebug",
                  action="store_true", dest="c_debug", default=False,
                  help="enable the crawler debug mode")
# dns set debug mode
parser.add_option("--ddebug",
                  action="store_true", dest="d_debug", default=False,
                  help="enable the dns set debug mode")

# firmware upgrade debubg mode
parser.add_option('--udebug',
                  action='store_true', dest='u_debug', default=False,
                  help='enable the upgrade debug mode')

(options, args) = parser.parse_args()

crawl_flag = options.crawl
dns_flag = options.dns
c_debug = options.c_debug
d_debug = options.d_debug
u_debug = options.u_debug

if (crawl_flag or dns_flag or c_debug or d_debug or u_debug) is False:
    print 'no mode chosen, program will exit'
    sys.exit(-1)

if c_debug:
    sys.path.append('./crawler')
    for arg in xrange(4):
        try:
            print args[arg]
        except Exception, e:
            print 'args should include ip, port, username, password'
            sys.exit(-1)
    test_crawl = CrawlerFactory(addr=args[0], port=int(args[1]),
                                username=args[2], password=args[3], debug=True)
    ret = test_crawl.produce()
    sys.exit(0)

if d_debug:
    sys.path.append('./dnsset')
    for arg in xrange(7):
        try:
            print args[arg]
        except Exception, e:
            print 'arg should include ip, port ,username, password, type, dns1, dns2'
            sys.exit(-1)
    target_dns = [args[5], args[6]]
    test_setter = DnssetFactory(addr=args[0], port=int(args[1]),
                                username=args[2], password=args[3],
                                type=args[4], dns=target_dns, debug=True)
    ret = test_setter.produce()
    sys.exit(0)

if u_debug:
    sys.path.append('./upgrade')
    for arg in xrange(6):
        try:
            print args[arg]
        except Exception:
            print 'arg should include ip, addr, port, username, password, type, firmware'
            sys.exit(-1)
    test_upgrader = UpgradeFactory(addr=args[0], port=args[1],
                                   username=args[2], password=args[3],
                                   type=args[4], firmware=args[5], debug=True)
    ret = test_upgrader.produce()
    sys.exit(0)

data_in_path = options.in_file_path
try:
    file(data_in_path)
except Exception, e:
    print 'no such ip address file'
    sys.exit(0)

data_out_path = options.out_file_path
threads_num = options.threads_num

if crawl_flag:
    sys.path.append('./crawler')
    work_manager = WorkManager(data_in_path, data_out_path, threads_num, 'crawl')
    work_manager.wait_all()
    sys.exit(0)

if dns_flag:
    sys.path.append('./dnsset')
    try:
        dns1 = args[0]
        dns2 = args[1]
    except Exception, e:
        print 'need two dns address to continue'
        sys.exit(-1)
    work_manager = WorkManager(data_in_path, data_out_path, threads_num, 'dns', dns1, dns2)
    work_manager.wait_all()
    sys.exit(0)
