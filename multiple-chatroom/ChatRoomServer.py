import socket
import select
import threading 
import time
import os
class ChatRoom():
    """
    init the ChatRoom Class
    """
    def __init__(self,host,port):
        
        self.host = host 
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

        self.client_dict = {} 
        # store all the clients, 
        # each element is username:[passwd,username]

    """
    return the time casually
    """
    def getTime(self):
        return time.ctime()[11:19]

    """
    start the ChatRoom 
    """
    def run(self):
        try:
            self.serversocket.bind(( self.host,self.port ))
            self.serversocket.listen(5)
        except socket.error,e:
            print e
            exit(0)

        ct = threading.Thread(process_client_thread,args=(self,))
        ct.start()
        mt = threading.Thread(process_msg_thread,args=(self,))
        mt.start()



        
    """
    a func to process the coming clients 
    """
    def process_client_thread(self):
        while(True):
            try:
                client,addr = self.serversocket.accept()
                rt = threading.Thread(register_thread,args=(self,client))
                rt.start()
            except socket.error,e:
                print e

        pass

    """
    a func to process the coming msg 
    """
    def process_msg_thread(self):
        pass 

    """
    broadcast the msg to all the client
    """
    def broadcast(self,msg):
        for c in self.client_dict:
            c_socket = self.client_dict[c][1]
            if( c_socket is not None):
                c_socket.send(msg)



    """
    a func to register a client
    :param client: the client socket which hasn't register 
    """
    def register_thread(self,client):
        re_str = "Please input your username:"
        client.send(re_str)
        data = client.recv(1024)
        username = data
        if username in self.client_dict:
            # already has this user, do login
            re_str = "Please input your passwd:"
            client.send(re_str)
            data = client.recv(1024)
            # check the passwd
            if(data == self.client_dict[username][0]):
                re_str="<%s>[%s] login successfully!" % (self.getTime(),username)
                self.broadcast(re_str)
                # add the client socket
                self.client_dict[username][1] = client
            else:
                # login failed
                re_str="Login failed: wrong passwd"
                client.send(re_str)
                os._exit(0) # exit the thread
        else:
            # not has this user, do register
            re_str="Please input the passwd for register:"
            client.send(re_str)
            data = client.recv(1024)
            passwd = data
            self.client_dict[username] = [passwd,client]


            


    def 





