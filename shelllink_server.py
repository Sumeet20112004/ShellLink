import socket
import sys
import os
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

        elif cmd[:4]=="pull":   
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
                print("file not found ",flush=True)
            else:
                print(str(conn.recv(1024),"utf-8"))
            response=str(conn.recv(1024),'utf-8')
            print(response,end=" ")

        elif cmd[:4]=="push":
            conn.send(str.encode(cmd))
            try:
                filesize = os.path.getsize(cmd[5:])
                conn.send(str(filesize).encode().ljust(16))    # function to make the bytestream 16 bytes
                with open(cmd[5:],'rb') as f:
                    out=f.read(1024)
                    while out:conn.send(out)
            except FileNotFoundError:
                conn.send(str(-1).encode().ljust(16))
                print("file not found ",flush=True)
            except Exception as e:
                conn.send(str(-2).encode().ljust(16))
                conn.send(str(e).encode())
                print("error : ",e,flush=True)
            response=str(conn.recv(1024),'utf-8')
            print(response,end=" ")
        elif len(cmd):
            conn.send(str.encode(cmd))
            response=str(conn.recv(1024),'utf-8')
            print(response,end=" ")



create_socket()
bind_socket()
accept()