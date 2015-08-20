August 18, 2015 5:11 PM
#####路由器类型匹配
|type_index|type|model|ID|fingerprint|weight|
|---|---|---|---|---|---|
|1|TP-Link|WR740N|3097|wr[\w]?740n|1|
#####DDL
```sql
CREATE TABLE INFO_MATCH (
ID INTEGER PRIMARY KEY REFERENCES MODULE_MATCH (ID) ON DELETE CASCADE ON UPDATE CASCADE, 
INFO_URL CHAR (128) NOT NULL, 
FIREWARE CHAR (128) NOT NULL, 
FIREWARE_INDEX INT NOT NULL, 
HARDWARE CHAR (128) NOT NULL, 
HARDWARE_INDEX INT NOT NULL, 
DNS CHAR (128) NOT NULL, 
DNS_INDEX INT (0) NOT NULL, 
AUTH_COOKIE CHAR (128) NOT NULL, 
OTHER_COOKIE CHAR (128) NOT NULL, 
REFERER CHAR (128) NOT NULL
);
```
#####路由器抓取信息匹配
|ID|info_url|firmware|fireware_index|hardware|hardware_index|dns|dns_index|auth_cookie|other_cookie|
|---|---|---|---|---|---|---|---|---|---|
|3097|/userRpm/Index.htm|var statusPara = new Array.+?"(.+?)"|1|var statusPara = new Array.+?".+?".+?"(.+?)"|1|var wanPara = new Array(.+?)"([\d\.]+? , [\d\.]+?)"|2|Authorization=Basic |tLargeScreenP=1; subType=pcSub; |
#####DDL
```sql
CREATE TABLE MODULE_MATCH (
ID INTEGER PRIMARY KEY AUTOINCREMENT, 
TYPE CHAR (50) NOT NULL, 
MODEL CHAR (50) NOT NULL, 
TYPE_INDEX INT NOT NULL, 
WEIGHT INT NOT NULL, 
FINGERPRINT CHAR (128)
);
```
