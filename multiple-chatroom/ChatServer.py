#coding=utf-8
import socket
import select
import select

addr = ("127.0.0.1",3000)
input_list = []
nickname_dict = {}

"""
create a new socket and listen
:rtype s:socket.socket()
"""
def conn():
    s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
            )
    s.bind(addr)
    s.listen(5)
    return s

"""
get the new coming client socket

:param ss:socket of server to monitor
:rtype 
"""
def new_coming(ss):
    client,address = ss.accept()
    print "new client coming..."
    wel_str="Welcome to the chating room.\nplease input your passwd:"
    client.send(wel_str)
    passwd = client.recv(1024)

    if passwd == "123":
        print "%s connect successfully!" % (str(address))
        client.send("Please input your nickname:")
        nickname = client.recv(1024)
        input_list.append(client)
        nickname_list[client] = nickname
        
    else:
        client.send("sys:Wrong passwd!")
        print "%s connect failed!" % (str(address))
        client.close()
            


"""
start the chatroom server
"""
def main():
    ss = conn()
    input_list.append(ss)
    while(True):
        rl,wl,el = select.select(input_list,[],[])
        for r in rl:
            if r is ss:
                #new client comging
                new_coming(ss)
            else:
                #new data from clients
                disconnect = False
                try:
                    data = r.recv((1024)
                    if data.strip()=="show list":
                        pass
                except socket.error,e:
                    print e
                    disconnect = True
                    

if(__name__=="__main__"):
    main()



