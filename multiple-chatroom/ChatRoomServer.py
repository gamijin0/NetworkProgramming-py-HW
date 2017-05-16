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

        # store all the clients, 
        # each element is username:[passwd,username]
        self.client_dict = {} 

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
        except e:
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
    a func to process the coming msg 
    """
    def process_msg_thread(self):
        print "Server start listening..." 
        while(True):
            client_list = list(map(lambda x: x[1],self.client_dict.values()))
            if(len(client_list)>0):
                #print client_list
                rl,wl,el = select.select(client_list,[],[])
                for r in rl:
                    data = r.recv(1024)
                    re_str = "<%s>[%s]Say:%s" % (self.getTime(),str(r),data)
                    self.broadcast(re_str,[r])

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
        re_str = "Please input your username:"
        client.send(re_str)
        data = client.recv(1024)
        username = data
        if username in self.client_dict:
            # already has this user, do login
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
                os._exit(0) # exit the thread
        else:
            # not has this user, do register
            re_str="You are a new user, please input a passwd for register:"
            client.send(re_str)
            data = client.recv(1024)
            passwd = data
            self.client_dict[username] = [passwd,client]
            re_str="<%s>[%s] register successfully!" % (self.getTime(),username)
            self.broadcast(re_str)
            




if(__name__=="__main__"):
    room = ChatRoom("127.0.0.1",3000)
    room.run()


