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
        et = etree.HTML(page)
        tr_xpath = "tbody//tr"
        trs = et.xpath(tr_xpath)
        for i in trs:
            print i
