import socket
import threading
import time
import os




class ChatRoomClient():
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def run(self):
        self.clientSocket.connect((self.host,self.port))
        lt = threading.Thread(target=self.listenMsg_thread,args=())
        lt.start()
        st = threading.Thread(target=self.sendMsg_thread,args=())
        st.start()


    """
    a thread func for listening and printing coming msg
    """
    def listenMsg_thread(self):
        while(True):
            try:
                data = self.clientSocket.recv(1024)
                if(len(data)==0):
                    print "Connection has broken."
                    os._exit(0)
                print data
            except Exception,e:
                print e

    """
    a thread func for send user msg 
    """
    def sendMsg_thread(self):
        while(True):
            time.sleep(0.2)
            msg = raw_input(">")
            if(msg=="quit"):
                self.clientSocket.close()
                os._exit(0)
            try:
                self.clientSocket.send(msg)
            except socket.error,e:
                print e

if(__name__=="__main__"):
    client = ChatRoomClient("127.0.0.1",3000)
    client.run()
