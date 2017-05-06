#coding: utf-8
import socket
import time
addr = ('127.0.0.1',3000)


if(__name__=="__main__"):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(addr)
    while(True):
        data = time.ctime()
        print "send [%s] to  [%s]" % (data,addr)
        client.send("Hello,the time is %s " % data)
        time.sleep(2)
