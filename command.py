#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan
# @Date:   2015-08-19 15:22:06
# @Last Modified by:   tan
# @Last Modified time: 2015-08-24 13:04:16

from optparse import OptionParser
from router_crawler import RouterCrawler
from thread_pool import WorkManager
import time
import sys

default_out_file = time.strftime("%m.%d-%H.%M.%S", time.localtime()) + '.csv'

parser = OptionParser()
#输入IP地址文件
parser.add_option("-i", "--input-file", dest="in_file_path",
                  help="IP address input file path", metavar="FILE")
#结果输出文件
parser.add_option("-o", "--output-file", dest="out_file_path", default=default_out_file,
                  help="scan output file path", metavar="FILE")
#线程数
parser.add_option("-t", "--threads", dest="threads_num", type="int", default=3,
                  help="scan theads num", metavar="NUM")

#启动信息抓取模式
parser.add_option("-c", "--crawl",
                  action="store_true", dest="crawl", default=False,  
                  help="enable the crawling mode")

#启动DNS设置模式
parser.add_option("-d", "--dns",
                  action="store_true", dest="dns", default=False,  
                  help="enable the dns set mode")

#启动调试模式
parser.add_option("--debug",
                  action="store_true", dest="debug", default=False,  
                  help="enable the debug mode")
# #调试模式下目标
# parser.add_option("--target", dest="debug_target_ip",
#                   help="the scan target under debug mode", metavar="IPADDR")

(options, args) = parser.parse_args()
#print options
#print args

crawl_flag = options.crawl
dns_flag = options.dns
debug_flag = options.debug

if ((crawl_flag or dns_flag or debug_flag) == False):
  print 'no mode choosen, program will exit'
  sys.exit(-1)

if debug_flag:
    # target_ip = args[0]
    # try:
    #     RouterCrawler.valid_ip(target)
    # except Exception, e:
    #     pass
    # else:
    for arg in xrange(3):
        try:
            print args[arg]
        except Exception, e:
            print 'args should include ip, port, username, passwd'
            sys.exit(-1)
    test_crawl = RouterCrawler(addr = args[0], port = int(args[1]), name = args[2], passwd = args[3], debug = True)
    ret = test_crawl.crawl()
    for (k, v) in ret.items():
        print '%s = ' % k, v
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
  work_manager =  WorkManager(data_in_path, data_out_path, threads_num, 'crawl')
  work_manager.wait_all()
  sys.exit(0)

if dns_flag:
  try:
    dns1 = args[0]
    dns2 = args[1]
  except Exception, e:
    print 'need two dns address to continue'
    sys.exit(-1)
  work_manager =  WorkManager(data_in_path, data_out_path, threads_num, 'dns', dns1, dns2)
  work_manager.wait_all()
  sys.exit(0)