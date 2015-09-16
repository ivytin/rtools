# router_info_scan

August 18, 2015 2:53 PM
- - -
A router infomation crawler with multithreading(thread pool) design. Also support setting dns automatically.

Working with: 
- TP-Link WR serial router
- DD-WRT
- D-Link ADSL
- D-Link DIR-505

To do:
- [ ] Add support for more types

- - -

#### usage：
```bash
$python command.py -h --help		view help
$python command.py --debug <ip_address> <port> <username> <password>		test router info crawling func
$python command.py -c -i <target csv file> [-o <result out file>] -t <thread_num>		crawling targets info
$python command.py -d -i <target csv file> -t <thread_num> <dns1> <dns2>		set targets dns
```
- - -
the input file for crawling should be csv format like following:
```csv
ip, port, username, password
```
the output file format：
```csv
ip, port, status, server, www-authentication, username, password, dns, type
14.199.15.34, 80, admin, admin, 202.120.2.101, dd_wrt
```

**Notice:** the last column *type* is the router model type detected by type_recognition.py, it will help the dns setting function to find the dns changing methods.

- - -
the input file for dns setting format:
```csv
ip, port, username, password, type
58.152.26.245, 80, admin, admin, dd_wrt
```