# router_info_scan

August 18, 2015 2:53 PM
- - -
A router information crawler with multiple threading (thread pool) design. And support automatic DNS setting.

#### Working with: 
- TP-Link WR serial router
- DD-WRT
- D-Link ADSL
- D-Link DIR-505

#### Lib:
- requests

#### To do:
- [ ] Add support for more types

- - -

#### usage：
```bash
$python command.py -h --help		view help
$python command.py --debug <ip_address> <port> <username> <password>		test router info crawling func
$python command.py -c -i <target csv file> [-o <result out file>] -t <thread_num>		crawling targets info
$python command.py -d -i <target csv file> -t <thread_num> <dns1> <dns2>		set targets dns
```

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


the input file for dns setting format:
```csv
ip, port, username, password, type
58.152.26.245, 80, admin, admin, dd_wrt
```
- - -

#### Sourcecode structure
```
├── crawler/
|   ├── base_crawler.py
|   ├── crawler_facotry.py
|   ├── tp_link_wr.py
|   ├── type_recognition.py
|   ├── ...
├── dnsset/
|   ├── base_setter.py
|   ├── dnsset_factory.py
|   ├── tp_link_wr.py
|   ├── ...
├── command.py
├── thread_pool.py
├── sqlite_crawler.py
```
When you need **add a crawler/dnsset plugin**, just extends the base class(base_crawler.py/base_setter.py). And rewrite the get_info/dns_set function.
For crawler plugin, you need modify type_recognition.py module, add regular expression for new router type

