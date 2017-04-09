#-*-coding utf-8-*-
from time import strftime,localtime
from socket import socket, AF_INET, SOCK_DGRAM

def  loggingWithTime(func):
    def wrapper(*args,**kwargs):
        print ("[%s] ========>> " % (strftime("%H:%M:%S"))),
        return func(*args,**kwargs)
    return wrapper



class UdpSocket(object):
    def __init__(self,host="127.0.0.1",port=2080):
        self.socket = socket(family=AF_INET,type=SOCK_DGRAM)
        self.host = host
        self.port = port

class UdpServer(UdpSocket):
    def __init__(self,*args,**kwargs):

        super(UdpServer, self).__init__(*args,**kwargs)

        self.BUFFERSIZE = 2048

        self.bind((self.host,self.port))
        self.listen((self.host,self.port))

    @loggingWithTime
    def bind(self,addr):
        print ("binding on %s" % str(addr))
        self.socket.bind(addr)


    @loggingWithTime
    def listen(self,addr):
        print ("listening on %s" % str(addr))
        while(True):
            data,addr = self.socket.recvfrom(self.BUFFERSIZE)
            self.socket.sendto()
            self.process(data,addr)

    @loggingWithTime
    def process(self,data,addr):
        print ("Get massage from %s : %s" % (addr,data) )


class UdpClient(UdpSocket):
    def __init__(self,*args,**kwargs):
        super(UdpClient, self).__init__(*args,**kwargs)
        self.interact()

    @loggingWithTime
    def interact(self):
        print "Please input msg to send:"
        while True:
            msg = raw_input()
            if not msg:
                break
            self.sendData(msg)


    @loggingWithTime
    def sendData(self,msg):
        print "Send: [%s] to %s " % (msg,str((self.host, self.port)))
        self.socket.sendto(msg, (self.host, self.port))


