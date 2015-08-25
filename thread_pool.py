#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: tan
# @Date:   2015-08-17 19:00:47
# @Last Modified by:   tan
# @Last Modified time: 2015-08-25 12:59:06

import csv
import requests
import Queue
import threading
import time
import socket
import sys
from router_crawler import RouterCrawler
from dns_payload import DNSPayload

class WorkManager(object):
    """线程池管理类，用于管理路由器抓取线程"""

    FUNC_NAME = ['crawl', 'dns']

    @staticmethod 
    def valid_ip(address):
        """验证IP是否合法"""
        try: 
            socket.inet_aton(address)
            return True
        except Exception, e:
            return False

    def __init__(self, data_in_path, data_out_path, thread_num, func, *dns):
        """初始化任务队列和线程队列"""
        self.file_lock = threading.Lock()
        self.work_queue = Queue.Queue()
        self.threads = []
        self.target_list = []
        target_num = self.data_in(data_in_path)
        #print target_num
        self.data_out_path = data_out_path
        self.__init_work_queue(func, target_num, self.target_list, *dns)
        self.__init_thread_pool(thread_num)

    def __init_work_queue(self, func, target_num, target_list, *dns):
        if func == 'crawl':
            print '-----crawl mode-----'
            for x in xrange(target_num):
                self.add_works(self.crawler, target_list[x])
        else:
            print '-----dns mode-----'
            for x in xrange(target_num):
                self.add_works(self.dns, [target_list[x], dns[0], dns[1]])

    def __init_thread_pool(self, thread_num):
        for x in xrange(thread_num):
            self.threads.append(Work(self.work_queue))
            #print len(self.threads)

    def crawler(self, target):
    #target sample: ['ip', port, 'username', 'passwd']
        #try:
        #print target
        try:
            crawler_thread = RouterCrawler(target[0], target[1], target[2], target[3])
            router_info = crawler_thread.crawl()
            self.data_out(self.data_out_path, router_info)
        except Error_addr, e:
            print e
        # for (k,v) in  router_info.items():
        #     print k, ' ', v

    def dns(self, target):
    #target sample: [['ip', port, 'username', 'passwd'], '8.8.4.4', '8.8.8.8']
        dns1 = target[1]
        dns2 = target[2]
        if self.valid_ip(dns1) == False or self.valid_ip(dns2) == False:
            print 'illegal dns address'
            sys.exit(-1)
        dns_thread = DNSPayload(target[0][0], target[0][1], target[0][2], target[0][3], target[0][4])
        dns_thread.dns_seting(dns1, dns2)

    def data_out(self, file_path, router_info):
        self.file_lock.acquire()
        csvfile = file(file_path, 'ab')
        writer = csv.writer(csvfile)
        router_row = []
        #由于Python字典是无序的，这里手动遍历，获得全部内容，格式如下
        # router_info = {
        #         'ip': ip,
        #         'port': port,
        #         'status': '',
        #         'router_server': '',
        #         'router_realm': '',
        #         'username': '',
        #         'passwd': '',
        #         'fm_version': '',
        #         'hm_version': '',
        #         'dns': '',
        #         'type_index': 0
        #         }
        columns = ['ip', 'port', 'status', 'router_server', 'router_realm', 'username', 'passwd', 'fm_version', 'hm_version', 'dns', 'type_index']
        try:
            for column in columns:
                if column in router_info:
                    router_row.append(router_info[column])
                else:
                    router_info.append('')
            writer.writerow(router_row)
        except Exception, e:
            pass
        csvfile.close()
        self.file_lock.release()

    def data_in(self, file_path):
        self.tartget_list = []
        csvfile = file(file_path, 'rb')
        reader = csv.reader(csvfile)
        row_len = 0
        for line in reader:
            target = []
            for x in xrange(len(line)):
                if x == 0:
                    if (self.valid_ip(line[0])):
                        target.append(line[0])
                        continue
                    else:
                        print 'line ' + str(row_len) + ': ip address error'
                        continue
                if x == 1:
                    if (0 < int(line[1]) and int(line[1]) < 65432):
                        target.append(80)
                        continue
                    else:
                        print 'line ' + str(row_len) + ': port error'
                        continue
                else:
                    target.append(line[x])
            self.target_list.append(target)
            row_len += 1
        return row_len

    def add_works(self, func, args):
        self.work_queue.put((func, args))

    def check_queue(self):
        return self.work_queue.qsize()

    def wait_all(self):
        for x in self.threads:
            while x.isAlive():
                #x.join()
                print self.check_queue(), 'threads reaming'
                time.sleep(5)

class Work(threading.Thread):
    """路由器信息抓取线程"""

    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                func, target = self.work_queue.get(block=False)
                func(target)
                self.work_queue.task_done()
            except Exception, e:
                #raise e
                #抛出异常，说明任务队列已经被清空
                break

if __name__ == '__main__':

    #data_in_path = './ip.csv'
    data_in_path = './dns.csv'
    data_out_path = './out.csv'
    work_manager =  WorkManager(data_in_path, data_out_path, 3, 'dns', '192.168.1.9', '192.168.2.3')
    work_manager.wait_all()
