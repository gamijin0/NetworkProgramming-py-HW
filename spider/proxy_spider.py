#coding=utf-8
import urllib
import urllib2
from lxml import etree

if(__name__=="__main__"):
    res = urllib.urlopen("http://www.ip181.com/")
    if(res.getcode()==200):
        print "Get page successfully, now parse the ip adresses"
        page = res.read().decode('gb2312')
    else:
        print "Get page failed! Please check the network "
    proxy_list = []
    et = etree.HTML(page)
    tr_xpath = "//tr"
    trs = et.xpath(tr_xpath)
    for i in trs:
        chs = i.getchildren()
	if len(chs)==7:
		u = dict(zip(["ip","port","is_transparent","link_type","lag","redion","update_time"],[ ch.text for ch in chs]))
		proxy_list.append(u)
		#ifor c in chs:
		#	print c.text
    
    for di in proxy_list[1:]:
        print "==========================="
        for k in di:
            print k,':',di[k]
