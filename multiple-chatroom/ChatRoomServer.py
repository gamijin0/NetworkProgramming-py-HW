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
        # store all the clients,
        # each element is username:[passwd,username]
        self.client_dict = {}

        self.client_list_lock = threading.RLock()

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

        pct = threading.Thread(target=self.process_client_thread,args=())
        pct.start()
        pmt = threading.Thread(target=self.process_msg_thread,args=())
        pmt.start()



        
    """
    a func to process the coming clients 
    """
    def process_client_thread(self):
        while(True):
            try:
                client,addr = self.serversocket.accept()
                print "[%s] try connecting..." % str(addr)
                rt = threading.Thread(target=self.register_thread,args=(client,))
                rt.start()
            except socket.error,e:
                print e


    """
    return all the client socket
    """
    def getAllClientSocket(self):
        client_list = []
        for k,v in self.client_dict.iteritems():
            if(v[1] is not None ):
                client_list.append(v[1])
        return client_list

    """
    get usernaem by one sock
    """
    def findUserbySocket(self,clientsock):
        for name in self.client_dict:
            if(self.client_dict[name][1]==clientsock):
                return name

    """
    remove one useless sock from the client_list
    """
    def removeSocket(self,sock):
        if(self.client_list_lock.acquire()):

            username = self.findUserbySocket(sock)
            re_str  = "<%s>[%s] has left the room." % (self.getTime(),username)
            self.client_dict[username][1] = None
            self.broadcast(re_str)

            self.client_list_lock.release()

    """
    a func to process the coming msg 
    """
    def process_msg_thread(self):
        print "Server start listening..." 
        while(True):
            client_list = self.getAllClientSocket()
            if(len(client_list)>0):
                #print client_list
                rl,wl,el = select.select(client_list,[],[])
                disconnect = False #use this flag to remove disconnect client
                for r in rl:
                        try:
                            data = r.recv(1024)
                            if(len(data)==0):
                                # len(data)==0   -->  socket has disconnected
                                self.removeSocket(r)
                                break
                            username = self.findUserbySocket(r)
                            re_str = "<%s>[%s]Say:%s" % (self.getTime(),username,data)
                            self.broadcast(re_str,[r])
                        except Exception,e:
                            print e
                            disconnect = True
                        if(disconnect):
                            self.removeSocket(r)

    """
    broadcast the msg to all the client
    """
    def broadcast(self,msg,except_list=[]):
        print msg
        for c in self.client_dict:
            if self.client_dict[c][1] in except_list:
                # not broacast to the user in block list
                continue
            c_socket = self.client_dict[c][1]
            if( c_socket is not None):
                c_socket.send(msg)



    """
    a func to register a client
    :param client: the client socket which hasn't register 
    """
    def register_thread(self,client):
        try:
            re_str = "Please input your username:"
            client.send(re_str)
            data = client.recv(1024)
            username = data
            if username in self.client_dict:
                # already has this user, do login

                if(self.client_dict[username][1] is not None):
                    re_str = "This account is being used!"
                    client.send(re_str)
                    return

                re_str = "You have registered, please input your passwd:"
                client.send(re_str)
                data = client.recv(1024)
                # check the passwd
                if(data == self.client_dict[username][0]):
                    re_str="<%s>[%s] login successfully!" % (self.getTime(),username)
                    self.broadcast(re_str)
                    # login successfully, update the client socket
                    self.client_dict[username][1] = client
                else:
                    # login failed
                    re_str="Login failed: wrong passwd"
                    client.send(re_str)
                    self.removeSocket(client)
            else:
                # not has this user, do register
                    re_str="You are a new user, please input a passwd for register:"
                    client.send(re_str)
                    data = client.recv(1024)
                    passwd = data
                    if(self.client_list_lock.acquire()):
                        self.client_dict[username] = [passwd,client]
                        self.client_list_lock.release()
                    re_str="<%s>[%s] register successfully!" % (self.getTime(),username)
                    self.broadcast(re_str)
        except Exception,e:
            print e

            




if(__name__=="__main__"):
    room = ChatRoom("127.0.0.1",3000)
    room.run()


