#coding=utf-8
import urllib
import urllib2
import threading
from lxml import etree


REGION_LIST = ['Brazil','China','America','Taiwan','Japan','Thailand','Vietnam','bahrein']
BASIC_URL = "http://www.proxy360.cn/Region/"


def get_proxy_ip_from(region):
    proxy_list = []
    if(type(region)!=str):
        print "Wrong type of region(must be str,now is %s)." % type(region)
        exit(0)
    else:
        print "Start fetching proxy_info form [%s]." % region

    rq = urllib2.Request(BASIC_URL+region)
    rq.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        'Host':'www.proxy360.cn',
    }
    response = urllib2.urlopen(rq)
    if(response.code==200):
        # print "Get data form [%s] successfully." % region
        html = response.read()
        div_path = "//div[@style='float:left; display:block; width:630px;']"
        et = etree.HTML(html.decode('utf-8'))
        divs = et.xpath(div_path)
        for div in divs:
            res = dict(
                        zip(
                            ['ip','port','is_transparent','region','date','today_score','total_score','day_to_live'],
                            [ch.text.strip() for ch in div.getchildren()]
                        )
                    )
            proxy_list.append(res)

        print "Get [%d] proxy from region [%s]" % (len(proxy_list),region)
        return proxy_list


def concurrent_start_spider():
    for region in REGION_LIST:
        th = threading.Thread(target=get_proxy_ip_from,args=[region],name=region)
        th.start()

    print "\n=========================================="



if(__name__=="__main__"):
    concurrent_start_spider()