#!/usr/bin/env python
# coding=utf-8
# author = zerokeeper
import requests
import re
import queue
import urllib3

urllib3.disable_warnings()

zhiwen = ''';notice! ';' is comment,'[]' is group.

[Langeuage]
Langeuage:php|headers|X-Powered-By|php
Langeuage:php|headers|Set-Cookie|PHPSSIONID
Langeuage:jsp|headers|Set-Cookie|JSESSIONID
Langeuage:asp|headers|Set-Cookie|ASPSESSION
Langeuage:aspx|headers|Set-Cookie|ASP.NET_SessionId
Langeuage:aspx|headers|X-AspNet-Version|version
Langeuage:aspx|index|index|<input[^>]+name=\"__VIEWSTATE
Langeuage:aspx|index|index|<a[^>]*?href=('|")[^http][^>]*?\.aspx(\?|\#|\1)
Langeuage:asp|index|index|<a[^>]*?href=('|")[^http][^>]*?\.asp(\?|\#|\1)
Langeuage:php|index|index|<a[^>]*?href=('|")[^http][^>]*?\.php(\?|\#|\1)
Langeuage:jsp|index|index|<a[^>]*?href=('|")[^http][^>]*?\.jsp(\?|\#|\1)

[Server]
Server:hadoop|index|index|<title>Hadoop Administration</title>
Server:elasticsearch|index|index|\"cluster_name\" : \"elasticsearch\"
Server:tomcat|index|index|<title>Apache Tomcat/.*?</title>
Server:hfs|headers|Set-Cookie|HFS_SID
Server:http_basic|headers|WWW-Authenticate|Basic

[Router]
Router:2wire|headers|Server|2wire
Router:2wire|headers|WWW-Authenticate|2wire
Router:3com||index|index|<META Detect1=\"Company\" CONTENT=\"3COM\">
Router:asmax|headers|WWW-Authenticate|Asmax
Router:asus|headers|WWW-Authenticate|Asus
Router:asus|index|index|<title>ASUS.*?Router.*?</title>
Router:d-link-dcs|headers|WWW-Authenticate|DCS-
Router:d-link-dir|headers|server|DIR-
Router:juniper|index|index|<title>Log In - Juniper Web Device Manager</title>
Router:linksys|headers|WWW-Authenticate|Basic realm=\"RT-
Router:linksys|index|index|<meta name=\"description\" content=\"Included with your Linksys Smart Wi-Fi Router.*?\">
Router:netcore|headers|WWW-Authenticate|NETCORE
Router:netgear|headers|WWW-Authenticate|NETGEAR
Router:technicolor|index|index|<img src=\"technicolor-logo.png\" alt=\"technicolor-logo\" .*?/>
Router:thomson|headers|WWW-Authenticate|Thomson
Router:tplink|headers|WWW-Authenticate|TP-LINK
Router:ubiquiti|index|index|<meta name=\"copyright\" content=\"Copyright.*?Ubiquiti.*?Networks.*?\">
Router:zte|headers|WWW-Authenticate|Basic realm=\"ZTE-
Router:h3c|headers|WWW-Authenticate|h3c
Router:h3c|index|index|<title>WEB Management Interface for H3C SecPath Series</title>| Hangzhou H3C
Router:huawei|headers|WWW-Authenticate|huawei

[camaera]
Camera:hikvision|headers|Server|Hikvision-Webs
Camera:hikvision|index|index|/doc/page/login.asp
Camera:hikvision|headers|Server|DVRDVS-Webs
Camera:hikvision|headers|server|DNVRS-Webs
Camera:hikvision|headers|server|App-webs
Camera:cctv|headers|Server|JAWS/1.0
Camera:web-service|index|index|<title>WEB SERVICE</title>
Camera:siemens-camera|index|index|<title>SIEMENS IP-Camera</title
Camera:samsoftech|index|index|Developed By :  <.*?>SAM Softech
Camera:zebra|index|index|<H1>Zebra Technologies<BR>
Camera:routeros|index|index|<title>RouterOS router configuration page<\/title>

[WAF]
WAF:Topsec-Waf|index|index|<META NAME="Copyright" CONTENT="Topsec Network Security Technology Co.,Ltd"/>|<META NAME="DESCRIPTION" CONTENT="Topsec web UI"/>
WAF:360|headers|X-Powered-By-360wzb|wangzhan\.360\.cn
WAF:360|url|/wzws-waf-cgi/|360wzws
WAF:Anquanbao|headers|X-Powered-By-Anquanbao|MISS
WAF:Anquanbao|url|/aqb_cc/error/|ASERVER
WAF:BaiduYunjiasu|headers|Server|yunjiasu-nginx
WAF:BigIP|headers|Server|BigIP|BIGipServer
WAF:BigIP|headers|Set-Cookie|BigIP|BIGipServer
WAF:BinarySEC|headers|x-binarysec-cache|fill|miss
WAF:BinarySEC|headers|x-binarysec-via|binarysec\.com
WAF:BlockDoS|headers|Server|BlockDos\.net
WAF:CloudFlare|headers|Server|cloudflare-nginx
WAF:Cloudfront|headers|Server|cloudfront
WAF:Cloudfront|headers|X-Cache|cloudfront
WAF:Comodo|headers|Server|Protected by COMODO
WAF:IBM-DataPower|headers|X-Backside-Transport|\A(OK|FAIL)
WAF:DenyAll|headers|Set-Cookie|\Asessioncookie=
WAF:dotDefender|headers|X-dotDefender-denied|1
WAF:Incapsula|headers|X-CDN|Incapsula
WAF:Jiasule|headers|Set-Cookie|jsluid=
WAF:KONA|headers|Server|AkamaiGHost
WAF:ModSecurity|headers|Server|Mod_Security|NOYB
WAF:NetContinuum|headers|Cneonction|\Aclose
WAF:NetContinuum|headers|nnCoection|\Aclose
WAF:NetContinuum|headers|Set-Cookie|citrix_ns_id
WAF:Newdefend|headers|Server|newdefend
WAF:NSFOCUS|headers|Server|NSFocus
WAF:Safe3|headers|X-Powered-By|Safe3WAF
WAF:Safe3|headers|Server|Safe3 Web Firewall
WAF:Safedog|headers|X-Powered-By|WAF/2\.0
WAF:Safedog|headers|Server|Safedog
WAF:Safedog|headers|Set-Cookie|Safedog
WAF:SonicWALL|headers|Server|SonicWALL
WAF:Stingray|headers|Set-Cookie|\AX-Mapping-
WAF:Sucuri|headers|Server|Sucuri/Cloudproxy
WAF:Usp-Sec|headers|Server|Secure Entry Server
WAF:Varnish|headers|X-Varnish|.*?
WAF:Varnish|headers|Server|varnish
WAF:Wallarm|headers|Server|nginx-wallarm
WAF:WebKnight|headers|Server|WebKnight
WAF:Yundun|headers|Server|YUNDUN
WAF:Yundun|headers|X-Cache|YUNDUN
WAF:Yunsuo|headers|Set-Cookie|yunsuo'''

class WebEye():

    def __init__(self, url):
        self.target = url
        self.tasks = queue.Queue()
        self.cms_list = set()
        self.read_config()

    def run(self):
        try:
            r = requests.get(self.target, timeout=15,verify=False)
            if r.encoding == "ISO-8859-1":
                encodings = requests.utils.get_encodings_from_content(r.text)
                if encodings:
                    encoding = encodings[0]
                else:
                    encoding = r.apparent_encoding

                encode_content = r.content.decode(encoding)
            else:
                encode_content = r.text
            self.headers = r.headers
            self.content = encode_content
        except:
            self.headers = ""
            self.content = ""

        self.discern()

    def title(self):
        m = re.search(r"<title>(.*)</title>",self.content,flags=re.I)
        if m:
            return m.group(1)
        return ""

    def read_config(self):
        mark_list = []
        config_file = zhiwen
        for mark in config_file.splitlines():
            # remove comment, group, blank line
            if re.match("\[.*?\]|^;", mark) or not mark.split():
                continue
            name, location, key, value = mark.strip().split("|", 3)
            mark_list.append([name, location, key, value])

        for mark_info in mark_list:
            self.tasks.put_nowait(mark_info)

    def discern(self):
        while not self.tasks.empty():
            mark_info = self.tasks.get()
            name, discern_type, key, reg = mark_info
            if discern_type == 'headers':
                self.discern_from_header(name, key, reg)
            elif discern_type == 'index':
                self.discern_from_index(name, reg)
            elif discern_type == "url":
                self.discern_from_url(name, key, reg)
            else:
                pass

    def discern_from_header(self, name, key, reg):
        if "Server" in self.headers:
            self.cms_list.add("Server:" + self.headers["Server"])
        if "X-Powered-By" in self.headers:
            self.cms_list.add("X-Powered-By:" + self.headers["X-Powered-By"])
        if key in self.headers and (re.search(reg, self.headers[key], re.I)):
            self.cms_list.add(name)
        else:
            pass

    def discern_from_index(self, name, reg):
        if re.search(reg, self.content, re.I):
            self.cms_list.add(name)
        else:
            pass

    def discern_from_url(self, name, key, reg):
        try:
            result = requests.get(self.target + key, timeout=15, verify=False)
            # time.sleep(0.5)
            if re.search(reg, result.content, re.I):
                self.cms_list.add(name)
            else:
                pass
        except Exception as e:
            # print e
            pass



def main():
    url = "https://x.hacking8.com"
    res = WebEye(url)
    res.run()
    cms = list(res.cms_list)
    # ['X-Powered-By:PHP/5.4.45', 'Langeuage:php', 'Server:nginx']
    print(cms)


if __name__ == '__main__':
    main()
