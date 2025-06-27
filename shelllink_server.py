import socket
import sys
def create_socket():
    try:
        global host
        host=""
        global port
        port=9999
        global s
        s=socket.socket()
    except socket.error as msg:
        print("socket creation error : ",msg)

def bind_socket():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("socket binding error : ",msg,'retrying')
        bind_socket()
        
def accept():
    conn,addr=s.accept()
    print("connection accepted form IP :",addr[0],"port :",str(addr[1]),sep=" ")
    send_command(conn)
    conn.close()
    s.close()
    sys.exit()

def send_command(conn):
    response=str(conn.recv(1024),'utf-8')
    print(response,end=" ")
    while True:
        cmd=input()
        if cmd=="exit":
            conn.send(str.encode(cmd))
            break
        elif cmd[:4]=="pull":   # still not complete if the client file ends it still does not close
            conn.send(str.encode(cmd))
            filesize=int(conn.recv(16).decode().strip())  #get the filesize
            if filesize>=0:
                received=0
                with open(cmd[5:],'wb') as f:
                    while received<filesize:
                        response=conn.recv(min(1024, filesize - received))
                        f.write(response)
                        received+=len(response)
            elif filesize==-1:
                print("file not found ")
            else:
                print(str(conn.recv(1024),"utf-8"))
            response=str(conn.recv(1024),'utf-8')
            print(response,end=" ")
        elif len(cmd):
            conn.send(str.encode(cmd))
            response=str(conn.recv(1024),'utf-8')
            print(response,end=" ")



create_socket()
bind_socket()
accept()