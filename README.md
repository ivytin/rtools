# router_info_scan

August 18, 2015 2:53 PM
- - -
A router infomation crawler with multithreading(thread pool) design. Also support setting dns automatically.

Working with: 
- TP-Link WR serial router
- DD-WRT
_ _ _

#### usage：
```bash
$python command.py -h --help		view help
$python command.py --debug <ip_addr> <port> <username> <passwd>		test router info crawling func
$python command.py -c -i <target csv file> [-o <result out file>] -t <thread_num>		crawling targets info
$python command.py -d -i <target csv file> -t <thread_num> <dns1> <dns2>		set targets dns
```
- - -
the input file for crawling should be csv format like following:
```csv
ip, port, username, passwd
```
the output file format：
```csv
ip, port, status, server, www-authentication, username, passwd, info, type_index
14.199.15.34, 80, admin, admin
```
**Notice: ** the last column *type-index* is the index number for this router type in the sqlite database, it will help the dns setting function to search the dns changing methods in the database.

- - -
the input file for dns setting format:
```csv
ip, port, username, passwd, type_index
58.152.26.245, 80, admin, admin, 2
```