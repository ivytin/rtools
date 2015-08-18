{
    "router_type": "TP-LINK TL-WR840N",
    "info_url": "/userRpm/Index.htm",
    "firmware": {"var statusPara = new Array.+?"(.+?)"": 1}
    "hardware": {"var statusPara = new Array.+?".+?".+?"(.+?)"": 1}
    "dns": {"var wanPara = new Array(.+?)"([\d\.]+? , [\d\.]+?)"": 2}
    "also_support": ["WR702N", "WR720N", "WR740N", "WR741N", "WR743N", "WR750N", "WR802N", "WR840N", "WR841N", "WR841HP", "WR842N", "WR843N", "WR940N", "WR941N"]
}

{
    "router_type": "DD_WRT",
    "info_url": "",
    "firmware": {"openAboutWindow.+?>(.+?)</a>": 1}
    "hardware": {">Capture\(status_router.sys_model.+?\n(.+?)&nbsp;": 1}
    "dns": {"": -1}
    "also_support": []
}