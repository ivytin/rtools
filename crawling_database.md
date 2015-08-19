August 18, 2015 5:11 PM
#####路由器类型匹配
|type_index|type|model|ID|fingerprint|weight|
|---|---|---|---|---|---|
|1|TP-Link|WR740N|3097|wr[\w]?740n|1|

#####路由器抓取信息匹配
|ID|info_url|firmware|fireware_index|hardware|hardware_index|dns|dns_index|auth_cookie|other_cookie|
|---|---|---|---|---|---|---|---|---|---|
|3097|/userRpm/Index.htm|var statusPara = new Array.+?"(.+?)"|1|var statusPara = new Array.+?".+?".+?"(.+?)"|1|var wanPara = new Array(.+?)"([\d\.]+? , [\d\.]+?)"|2|Authorization=Basic |tLargeScreenP=1; subType=pcSub; |
