#coding: utf-8
import select
import socket

addr = ('127.0.0.1',3000)

if(__name__=="__main__"):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    read_list = []
    read_list.append(server)
    server.bind(addr)
    server.listen(5)

    while(True):
        rl, wl, el = select.select(read_list, [], [])
        for r in rl:
            if (r is server): #处理到来的tcp连接

                conn,addr = server.accept()
                print "Got a connection from ",addr
                read_list.append(conn)

            else: #处理到来的tcp消息
                try:
                    data = r.recv(1024)
                    disconnected = not  data
                except socket.error,e:
                    print e
                    disconnected = True

                if(disconnected is True):
                    print r.getpeername(),"disconnected."
                    read_list.remove(r)
                else:
                    print "Recv: [%s] from [%s]" % (data,r.getpeername())


