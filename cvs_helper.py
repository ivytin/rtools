#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'

import csv
import sys

class CsvHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def combine_file(path_lft, path_rht, path_out='combine_out.csv'):
        file_lft = open(path_lft, 'rb')
        file_rht = open(path_rht, 'rb')
        file_out = open(path_out, 'ab')
        reader_lft = csv.reader(file_lft)
        reader_rht = csv.reader(file_rht)
        writer_out = csv.writer(file_out)

        list_lft = []
        list_rht = []
        for line in reader_lft:
            list_lft.append(line)
        for line in reader_rht:
            list_rht.append(line)
        list_lft.sort(key=lambda x: x[0])
        list_rht.sort(key=lambda x: x[0])

        for i in xrange(len(list_lft)):
            # print list_lft[i][0], list_rht[i][0]
            if list_lft[i][2] == 'success':
                writer_out.writerow(list_lft[i])
                continue
            elif list_rht[i][2] == 'success':
                writer_out.writerow(list_rht[i])
                continue
            if list_lft[i][2] == '':
                writer_out.writerow(list_lft[i])
                continue
            elif list_rht[i][2] == '':
                writer_out.writerow(list_rht[i])
                continue
            if list_lft[i][2] == 'unknown type':
                writer_out.writerow(list_lft[i])
                continue
            elif list_rht[i][2] == 'unknown type':
                writer_out.writerow(list_rht[i])
                continue
            else:
                writer_out.writerow(list_lft[i])

        print 'combine file finish'

if __name__ == '__main__':
    csv_helper = CsvHelper()
    csv_helper.combine_file(sys.argv[1], sys.argv[2])
